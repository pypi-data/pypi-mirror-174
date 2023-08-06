#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from csv import writer
import os
import copy
import yaml
import math
import numpy as np
from collections import OrderedDict, UserDict
from .query import QueryBackendCapability
from .adaptor import adaptor_registry, Adaptor
from ..utils.utility import LazyImport, CpuInfo, singleton, Dequantize, dump_elapsed_time
from ..utils.utility import Statistics, GLOBAL_STATE, MODE, version1_lt_version2
from ..utils import logger
from ..conf.dotdict import deep_get
from ..experimental.data.dataloaders.base_dataloader import BaseDataLoader

tensorflow = LazyImport('tensorflow')

@adaptor_registry
class TensorFlowAdaptor(Adaptor):
    unify_op_type_mapping = {
        "Conv2D": "conv2d",
        "Conv3D": "conv3d",
        "DepthwiseConv2dNative": "conv2d",
        "FusedBatchNormV3": "batchnorm",
        "_MklFusedInstanceNorm": "instancenorm",
        "MaxPool": "pooling",
        "MaxPool3D": "pooling",
        "AvgPool": "pooling",
        "ConcatV2": "concat",
        "MatMul": "matmul",
        "BatchMatMul": "matmul",
        "BatchMatMulV2": "matmul",
        "Pad": "pad",
        "Conv2DBackpropInput": "deconv2d",
        "Conv3DBackpropInputV2": "deconv3d"
    }
    def __init__(self, framework_specific_info):
        super().__init__(framework_specific_info)

        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ['CUDA_VISIBLE_DEVICES'] = "-1"
        self.quantize_config = {'op_wise_config': {}}
        self.framework_specific_info = framework_specific_info
        self.approach = deep_get(self.framework_specific_info, 'approach', False)
        self.device = self.framework_specific_info['device']
        self.work_dir = os.path.abspath(self.framework_specific_info['workspace_path'])
        self.recipes = deep_get(self.framework_specific_info, 'recipes', {})
        self.performance_only = deep_get(self.framework_specific_info, 'performance_only', False)
        os.makedirs(self.work_dir, exist_ok=True)

        self.pre_optimized_model = None
        self.pre_optimizer_handle = None

        self.bf16_ops = []
        self.fp32_ops = []
        self.dump_times = 0   # for tensorboard

        cfg_yaml_name = "{}.yaml".format(self.__class__.__name__[:-len('Adaptor')].lower())
        self.query_handler = TensorflowQuery(local_config_file=os.path.join(
            os.path.dirname(__file__), cfg_yaml_name), performance_only=self.performance_only)
        self.itex_mode = cfg_yaml_name == 'tensorflow_itex.yaml'

        from pkg_resources import parse_version
        import tensorflow as tf
        self.new_api = True if parse_version(tf.version.VERSION) == parse_version('2.11.0202242') else False
        self.qdq_enabled = cfg_yaml_name == 'tensorflow_itex.yaml' or self.new_api
        self.op_wise_sequences = self.query_handler.get_eightbit_patterns(self.qdq_enabled)
        self.optimization = self.query_handler.get_grappler_optimization_cfg()

        self.fp32_results = []
        self.fp32_preds_as_label = False
        self.benchmark = (GLOBAL_STATE.STATE == MODE.BENCHMARK)
        self.callbacks = []

        self.optype_statistics = None

    def log_histogram(self, writer, tag, values, step=0, bins=1000):
        import tensorflow as tf
        # Convert to a numpy array
        values = np.array(values)

        # Create histogram using numpy
        # counts, bin_edges = np.histogram(values, bins=bins)

        # Fill fields of histogram proto
        # hist = tf.compat.v1.HistogramProto()
        # hist.min = float(np.min(values))
        # hist.max = float(np.max(values))
        # hist.num = int(np.prod(values.shape))
        # hist.sum = float(np.sum(values))
        # hist.sum_squares = float(np.sum(values**2))

        # bin_edges = bin_edges[1:]

        # for edge in bin_edges:
        #     hist.bucket_limit.append(edge)
        # for c in counts:
        #     hist.bucket.append(c)

        # Create and write Summary
        # update using TF2.X API
        with writer.as_default():
            tf.summary.histogram(tag, values, step)
            writer.flush()

    def _pre_hook_for_hvd(self, dataloader=None):
        import horovod.tensorflow as hvd
        self.hvd = hvd
        self.hvd.init()

    @dump_elapsed_time(customized_msg="Model training")
    def train(self, model, dataloader, optimizer_tuple,
              criterion_tuple, hooks, postprocess, **kwargs):
        # check model is savedmodel or not
        import tensorflow as tf
        from neural_compressor.model.model import get_model_type
        tf.random.set_seed(1)
        self.model_type = get_model_type(model._model)
        optimizer = optimizer_tuple[0](**optimizer_tuple[1])
        criterion = criterion_tuple[0](**criterion_tuple[1])
        start_epochs = kwargs['kwargs'].get('start_epoch', None)
        end_epochs = kwargs['kwargs'].get('end_epoch', None)
        epochs = kwargs['kwargs'].get('epoch', None)
        iters = kwargs['kwargs'].get('iteration', None)
        callbacks = kwargs['kwargs'].get('callbacks', None)
        execution_mode = kwargs['kwargs'].get('execution_mode', None)
        distributed = getattr(dataloader, 'distributed', False)
        from neural_compressor.experimental.common.criterion import TensorflowKnowledgeDistillationLoss
        if isinstance(criterion, TensorflowKnowledgeDistillationLoss):
            input_model = model._model
        else:
            input_model = tf.keras.models.load_model(model._model)
            hooks = callbacks['tf_pruning'](model, input_model, hooks)
        hooks['on_train_begin']()                 # on_train_begin hook
        train_loss_results = []
        if distributed:
            try:
                len_dataloader = len(dataloader)
            except:
                logger.info("The length of the distributed training dataloader is unknown."
                            "When the iteration of training dataloader in each process is "
                            "inconsistent, an error may occur.")
            else:
                list_len_dataloader = self.hvd.allgather_object(len_dataloader)
                if self.hvd.rank() == 0:
                    for i in range(len(list_len_dataloader)-1):
                        if list_len_dataloader[i] != list_len_dataloader[i+1]:
                            raise AttributeError("The traning dataloader's iteration is"
                                                "different between processes, please reset dataloader's batch_size.")

        def training_step(x, y, first_batch):
            with tf.GradientTape() as tape:
                tape.watch(input_model.trainable_variables)
                y_ = input_model(x, training=True)
                loss_value = criterion(y, y_)
                loss_value = hooks['on_after_compute_loss'](x, y_, loss_value)
            tape = self.hvd.DistributedGradientTape(tape) if distributed else tape
            # Get gradient
            grads = tape.gradient(loss_value, input_model.trainable_variables) # pylint: disable=no-member
            # Optimize the model
            optimizer.apply_gradients(zip(grads, input_model.trainable_variables)) # pylint: disable=no-member
            if distributed and first_batch:
                self.hvd.broadcast_variables(input_model.variables, root_rank=0)
                self.hvd.broadcast_variables(optimizer.variables(), root_rank=0)
            return loss_value

        training_step = training_step if execution_mode=='eager' else tf.function(training_step)
        if start_epochs is not None and end_epochs is not None:
            epochs = end_epochs - start_epochs
        for epoch in range(epochs):
            cnt = 0
            epoch_loss_avg = tf.keras.metrics.Mean()
            hooks['on_epoch_begin'](epoch)         # on_epoch_begin hook
            # Training loop
            for iter, data in enumerate(dataloader):
                x, y = postprocess(data) if postprocess is not None else data
                hooks['on_step_begin'](iter)      # on_step_begin hook
                cnt += 1
                loss_value = training_step(x, y, iter==0)
                # Track progress
                epoch_loss_avg.update_state(loss_value)  # Add current batch loss
                hooks['on_step_end']()            # on_step_end hook
                if iters is not None and cnt >= iters:
                    break
            model._sess = None
            hooks['on_epoch_end']()                # on_epoch_end hook
            # End epoch
            train_loss_results.append(epoch_loss_avg.result())
            if distributed:
                logger.info("Epoch-{:03d} training on rank {!s} have been done." \
                    .format(epoch+1, self.hvd.allgather_object(self.hvd.rank())))
            logger.info("Epoch {:03d}: Loss: {:.3f}".format(epoch+1, epoch_loss_avg.result()))

        hooks['on_train_end']()                  # on_train_end hook
        model._sess = None
        if not isinstance(criterion, TensorflowKnowledgeDistillationLoss):
            if distributed:
                if self.hvd.rank() == 0:
                    # Update the input model with pruned weights manually due to keras API limitation.
                    input_model.save(model._model)
                rank_list = self.hvd.allgather_object(self.hvd.rank())
                logger.info(f"rank 0 has saved the pruned model to '{model._model}',"
                            f"all ranks {rank_list} ready.")
            else:
                input_model.save(model._model)
        else:
            input_model.save('distillation_model')

    @dump_elapsed_time(customized_msg="Model inference")
    def evaluate(self, model, dataloader, postprocess=None,
                 metrics=None, measurer=None, iteration=-1,
                 tensorboard=False, fp32_baseline=False):
        """Evaluate the model for specified metric on validation dataset.

        Args:
            model ([Graph, GraphDef or Path String]): The model could be the graph,
                        graph_def object, the frozen pb or ckpt/savedmodel folder path.
            dataloader (generator): generate the data and labels.
            postprocess (object, optional): process the result from the model
            metrics (list, optional): Depends on model category. Defaults to None.
            measurer (object, optional): for precise benchmark measurement.
            iteration(int, optional): control steps of mini-batch
            tensorboard (boolean, optional): for tensorboard inspect tensor.
            fp32_baseline (boolen, optional): only for compare_label=False pipeline

        Returns:
            [float]: evaluation result, the larger is better.
        """
        import tensorflow as tf
        from .tf_utils.util import iterator_sess_run
        outputs = model.output_tensor_names

        if getattr(dataloader, 'distributed', False):
            import horovod.tensorflow as hvd
            hvd.init()
            # If metric.hvd is not None then run distributed inference
            for metric in metrics:
                metric.hvd = hvd
            try:
                len_dataloader = len(dataloader)
            except:
                logger.info("The length of the distributed evaluation dataloader is unknown."
                            "When the iteration of evaluation dataloader in each process is "
                            "inconsistent, an error may occur.")
            else:
                list_len_dataloader = hvd.allgather_object(len_dataloader)
                if hvd.rank() == 0:
                    for i in range(len(list_len_dataloader)-1):
                        if list_len_dataloader[i] != list_len_dataloader[i+1]:
                            raise AttributeError("The evaluation dataloader's iteration is"
                                                 "different between processes, please reset dataloader's batch_size.")
            logger.info("Rank {!s} dataloaders' data distribution balance check for evaluation have been finnished." \
                .format(hvd.allgather_object(hvd.rank())))
        if tensorboard:
            from .tf_utils.graph_util import GraphAnalyzer
            from tensorflow.python.framework import tensor_util

            output_postfix = "_fp32.output"
            inspect_node_types = ["Conv2D", "DepthwiseConv2dNative", "MaxPool", "AvgPool",
                                  "ConcatV2", "MatMul", "FusedBatchNormV3", "FusedBatchNorm", "BiasAdd",
                                  "_MklFusedInstanceNorm", "Relu", "Relu6", "Dequantize"]
            fp32_inspect_node_name = []
            int8_inspect_node_name = []
            q_node_scale = {}
            if self.dump_times == 0:
                temp_dir = "./runs/eval/baseline"
            else:
                temp_dir = "./runs/eval/tune_" + str(self.dump_times)
            if os.path.isdir(temp_dir):
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            # Create the writer using TF2.x APIs to handle eager excutions
            writer = tf.summary.create_file_writer(temp_dir) # pylint: disable=no-member
            with writer.as_default():
                tf.summary.graph(model.graph) # pylint: disable=no-member

            cur_graph = GraphAnalyzer()
            cur_graph.graph = model.graph_def
            cur_graph.parse_graph()
            graph_info = cur_graph.node_name_details
            for node in model.graph_def.node:
                if node.op in inspect_node_types:
                    fp32_inspect_node_name.append(node.name)
                # Tensor dump supported quantized op including,
                # Requantize, QuantizedConv2DAndRequantize,
                # QuantizedConv2DAndReluAndRequantize,
                # QuantizedConv2DWithBiasAndRequantize,
                # QuantizedConv2DWithBiasAndReluAndRequantize,
                # QuantizedConv2DWithBiasSignedSumAndReluAndRequantize,
                # QuantizedConv2DWithBiasSumAndReluAndRequantize,
                # QuantizedDepthwiseConv2DWithBiasAndReluAndRequantize,
                # QuantizedMatMulWithBiasAndReluAndRequantize,
                # QuantizedMatMulWithBiasAndRequantize
                elif node.op.find("Requantize") != -1:
                    out_min = -2
                    out_max = -1
                    if node.op.find("Sum") != -1:
                        out_min = -5
                        out_max = -4
                    q_out_min = graph_info[node.input[out_min]
                                           ].node.attr["value"].tensor.float_val[0]
                    q_out_max = graph_info[node.input[out_max]
                                           ].node.attr["value"].tensor.float_val[0]
                    q_node_scale[node.name] = (node.op, q_out_min, q_out_max)
                    int8_inspect_node_name.append(node.name)
                # Inspect weights, bias. Need further optimize
                if node.op == "Const" and graph_info[graph_info[node.name].outputs[0]].node.op \
                    in ["Conv2D", "DepthwiseConv2dNative", "MatMul",
                    "FusedBatchNormV3", "_MklFusedInstanceNorm", "BiasAdd"]:
                    const_value = tensor_util.MakeNdarray(node.attr.get(
                                  'value').tensor).astype(np.float32)
                    self.log_histogram(writer, node.name, const_value)

            outputs.extend(fp32_inspect_node_name)
            if len(int8_inspect_node_name) > 0:
                output_postfix = "_int8.output"
                outputs.extend(int8_inspect_node_name)

        if metrics:
            for metric in metrics:
                metric.reset()
            self.fp32_preds_as_label = any([hasattr(metric, "compare_label") and \
                not metric.compare_label for metric in metrics])

        origin_output_tensor_names = model.output_tensor_names
        model.output_tensor_names = outputs
        input_tensor = model.input_tensor
        output_tensor = model.output_tensor if len(model.output_tensor)>1 else \
                            model.output_tensor[0]
        logger.info("Start to evaluate the TensorFlow model.")

        def eval_func(dataloader):
            results = []
            for idx, (inputs, labels) in enumerate(dataloader):
                # dataloader should keep the order and len of inputs same with input_tensor
                if len(input_tensor) == 1:
                    feed_dict = {}
                    if isinstance(inputs, dict) or isinstance(inputs, OrderedDict) \
                      or isinstance(inputs, UserDict):
                        for name in inputs:
                            for tensor in input_tensor:
                                pos = tensor.name.rfind(":")
                                t_name = tensor.name if pos < 0 else tensor.name[:pos]
                                if name == t_name:
                                    feed_dict[tensor] = inputs[name]
                                    break
                    else:
                        feed_dict = {input_tensor[0]: inputs}  # get raw tensor using index [0]
                else:
                    assert len(input_tensor) == len(inputs), \
                        'inputs len must equal with input_tensor'
                    feed_dict = {}
                    if isinstance(inputs, dict) or isinstance(inputs, OrderedDict) \
                      or isinstance(inputs, UserDict):
                        for name in inputs:
                            for tensor in input_tensor:
                                pos = tensor.name.rfind(":")
                                t_name = tensor.name if pos < 0 else tensor.name[:pos]
                                if name == t_name:
                                    feed_dict[tensor] = inputs[name]
                                    break
                    else:
                        feed_dict = dict(zip(input_tensor, inputs))

                if model.iter_op:
                    predictions = iterator_sess_run(model.sess, model.iter_op, \
                        feed_dict, output_tensor, iteration, measurer)
                elif measurer is not None:
                    measurer.start()
                    predictions = model.sess.run(output_tensor, feed_dict)
                    measurer.end()
                else:
                    predictions = model.sess.run(output_tensor, feed_dict)

                if self.fp32_preds_as_label:
                    self.fp32_results.append(predictions) if fp32_baseline else \
                        results.append(predictions)

                # Inspect node output, just get 1st iteration output tensors for now
                if idx == 0 and tensorboard:
                    for index, node_name in enumerate(outputs):
                        tensor = predictions[index]
                        if node_name in int8_inspect_node_name:
                            tensor = Dequantize(predictions[index], q_node_scale[node_name])
                        self.log_histogram(writer, node_name + output_postfix, tensor.astype(
                                           np.float32), idx)
                    writer.close()
                if isinstance(predictions, list):
                    if len(origin_output_tensor_names) == 1:
                        predictions = predictions[0]
                    elif len(origin_output_tensor_names) > 1:
                        predictions = predictions[:len(origin_output_tensor_names)]
                if postprocess is not None:
                    predictions, labels = postprocess((predictions, labels))
                if metrics:
                    for metric in metrics:
                        if not hasattr(metric, "compare_label") or \
                            (hasattr(metric, "compare_label") and metric.compare_label):
                            metric.update(predictions, labels)
                if idx + 1 == iteration:
                    break
            return results

        if isinstance(dataloader, BaseDataLoader) and not self.benchmark:
            try:
                results = eval_func(dataloader)
            except Exception:  # pragma: no cover
                logger.warning(
                    "Fail to forward with batch size={}, set to {} now.".
                    format(dataloader.batch_size, 1))
                dataloader.batch(1)
                results = eval_func(dataloader)
        else:  # pragma: no cover
            results = eval_func(dataloader)

        if self.fp32_preds_as_label:
            from .tf_utils.util import collate_tf_preds
            if fp32_baseline:
                results = collate_tf_preds(self.fp32_results)
                reference = results
            else:
                reference = collate_tf_preds(self.fp32_results)
                results = collate_tf_preds(results)
            for metric in metrics:
                if hasattr(metric, "compare_label") and not metric.compare_label:
                    metric.update(results, reference)

        acc = 0 if metrics is None else [metric.result() for metric in metrics]
        if tensorboard:
            new_dir = temp_dir + "_acc_" + str(acc)
            writer.close()
            if os.path.isdir(new_dir):
                import shutil
                shutil.rmtree(new_dir, ignore_errors=True)
            os.rename(temp_dir, new_dir)
            self.dump_times += 1
        model.output_tensor_names = origin_output_tensor_names
        return acc if not isinstance(acc, list) or len(acc) > 1 else acc[0]

    def tuning_cfg_to_fw(self, tuning_cfg):
        """Parse the neural_compressor wrapped configuration to Tensorflow.

        Args:
            tuning_cfg (dict): configuration for quantization.
        """
        self.quantize_config['calib_iteration'] = tuning_cfg['calib_iteration']
        self.quantize_config['device'] = self.device
        self.quantize_config['advance'] = deep_get(tuning_cfg, 'advance')
        fp32_ops = []
        bf16_ops = []
        dispatched_op_names = [j[0] for j in tuning_cfg['op']]

        invalid_op_names = [i for i in self.quantize_config['op_wise_config']
                            if i not in dispatched_op_names]

        for op_name in invalid_op_names:
            self.quantize_config['op_wise_config'].pop(op_name)

        for each_op_info in tuning_cfg['op']:
            op_name = each_op_info[0]

            if tuning_cfg['op'][each_op_info]['activation']['dtype'] in ['fp32', 'bf16']:
                if op_name in self.quantize_config['op_wise_config']:
                    self.quantize_config['op_wise_config'].pop(op_name)
                if tuning_cfg['op'][each_op_info]['activation']['dtype'] == 'fp32':
                    fp32_ops.append(op_name)
                if tuning_cfg['op'][each_op_info]['activation']['dtype'] == 'bf16':
                    bf16_ops.append(op_name)
                continue

            is_perchannel = False
            bit = None
            if 'weight' in tuning_cfg['op'][each_op_info]:
                is_perchannel = tuning_cfg['op'][each_op_info]['weight'][
                    'granularity'] == 'per_channel'
                #bit = tuning_cfg['op'][each_op_info]['weight']['bit']
            weight_bit = bit if bit else 7.0

            algorithm = tuning_cfg['op'][each_op_info]['activation']['algorithm']

            is_asymmetric = False
            if 'activation' in tuning_cfg['op'][each_op_info]:
                is_asymmetric = tuning_cfg['op'][each_op_info]['activation']['scheme'] == 'asym'
            self.quantize_config['op_wise_config'][op_name] = (is_perchannel,
                                                               algorithm,
                                                               is_asymmetric,
                                                               weight_bit)
        self.fp32_ops = fp32_ops
        self.bf16_ops = bf16_ops

    @dump_elapsed_time("Pass quantize model")
    def quantize(self, tune_cfg, model, data_loader, q_func=None):
        """Execute the quantize process on the specified model.

        Args:
            tune_cfg (dict): quantization configuration
            model (tf.compat.v1.GraphDef): fp32 model
            data_loader (generator): generator the data and labels
            q_func (optional): training function for quantization aware training mode,
                                which not enabled for tensorflow yet.

        Returns:
            tf.compat.v1.GraphDef: the quantized model
        """
        if self.approach == "quant_aware_training":
            assert q_func is not None, "quantization aware training mode \
                is not configured correctly"

            from neural_compressor.experimental import common
            qat_model = q_func(model)

            return self.convert(common.Model(qat_model), 'QAT', 'default')

        assert q_func is None, \
            "post-training quantization mode is not support calibration function for Tensorflow!"
        self.tuning_cfg_to_fw(tune_cfg)
        logger.debug("Dump quantization configurations:")
        logger.debug(self.quantize_config)
        from .tf_utils.graph_converter import GraphConverter
        calib_sampling_size = tune_cfg.get('calib_sampling_size', 1)
        if isinstance(data_loader, BaseDataLoader):
            batch_size = data_loader.batch_size
            try:
                for i in range(batch_size):
                    if calib_sampling_size % (batch_size - i) == 0:
                        calib_batch_size = batch_size - i
                        if i != 0:  # pragma: no cover
                            logger.warning("Reset `calibration.dataloader.batch_size` field "
                                           "to {}".format(calib_batch_size) +
                                           " to make sure the sampling_size is "
                                           "divisible exactly by batch size")
                        break
                tmp_iterations = int(math.ceil(calib_sampling_size / calib_batch_size))
                data_loader.batch(calib_batch_size)
                self.quantize_config['calib_iteration'] = tmp_iterations
                converted_model = GraphConverter(model,
                                        qt_config=self.quantize_config,
                                        recipes=self.recipes,
                                        int8_sequences=self.op_wise_sequences,
                                        fp32_ops=self.fp32_ops,
                                        bf16_ops=self.bf16_ops,
                                        data_loader=data_loader,
                                        qdq_enabled=self.qdq_enabled,
                                        new_api=self.new_api,
                                        performance_only = self.performance_only).convert()
            except Exception: # pragma: no cover
                from .tf_utils.util import get_model_input_shape
                batch_size = get_model_input_shape(model)
                logger.warning(
                        "Fail to forward with batch size={}, set to {} now.".
                        format(data_loader.batch_size, batch_size))
                data_loader.batch(batch_size)
                self.quantize_config['calib_iteration'] = calib_sampling_size
                converted_model = GraphConverter(model,
                                        qt_config=self.quantize_config,
                                        recipes=self.recipes,
                                        int8_sequences=self.op_wise_sequences,
                                        fp32_ops=self.fp32_ops,
                                        bf16_ops=self.bf16_ops,
                                        data_loader=data_loader,
                                        qdq_enabled=self.qdq_enabled,
                                        new_api=self.new_api,
                                        performance_only = self.performance_only).convert()
        else: # pragma: no cover
            if hasattr(data_loader, 'batch_size') and \
              calib_sampling_size % data_loader.batch_size != 0:
                iter = self.quantize_config['calib_iteration']
                logger.warning(
                    "Please note that calibration sampling size {} " \
                    "isn't divisible exactly by batch size {}. " \
                    "So the real sampling size is {}.".
                    format(calib_sampling_size, data_loader.batch_size,
                           data_loader.batch_size * iter))
            converted_model = GraphConverter(model,
                                qt_config=self.quantize_config,
                                recipes=self.recipes,
                                int8_sequences=self.op_wise_sequences,
                                fp32_ops=self.fp32_ops,
                                bf16_ops=self.bf16_ops,
                                data_loader=data_loader,
                                qdq_enabled=self.qdq_enabled,
                                new_api=self.new_api,
                                performance_only = self.performance_only).convert()
        #just save framework_specific_info feature for recover
        converted_model.q_config.update({'framework_specific_info': \
                                            self.framework_specific_info})

        self._dump_model_op_stats(converted_model.graph_def)

        return converted_model

    def _dump_model_op_stats(self, model_graphdef):
        fp32_op_list_uint8 = copy.deepcopy(
            self.query_handler.get_op_types_by_precision(precision='uint8'))
        fp32_op_list_int8 = copy.deepcopy(
            self.query_handler.get_op_types_by_precision(precision='int8'))
        fp32_op_list=list(set(fp32_op_list_uint8).union(set(fp32_op_list_int8)))


        int8_op_prefix_list = ['QuantizedConv2D', '_FusedQuantizedConv3D', 'QuantizedDepthwise',
                               'QuantizedMaxPool', 'QuantizedAvgPool',
                               'QuantizedConcatV2', 'QuantizedMatMul',
                               '_QuantizedFusedBatchNorm', '_QuantizedMatMul',
                               '_QuantizedBatchMatMul', '_QuantizedFusedInstanceNorm',
                               '_FusedQuantizedDeconv2D', '_FusedQuantizedDeconv3D']
        from tensorflow.python.framework import dtypes

        res = {}
        for op_type in fp32_op_list:
            res[op_type] = {'INT8': 0, 'BF16': 0, 'FP32': 0}
        res['QuantizeV2'] = {'INT8': 0, 'BF16': 0, 'FP32': 0}
        res['Dequantize'] = {'INT8': 0, 'BF16': 0, 'FP32': 0}
        res['Cast'] = {'INT8': 0, 'BF16': 0, 'FP32': 0}
        fp32_op_list.extend(['QuantizeV2', 'Dequantize', 'Cast'])
        for i in model_graphdef.node:
            if i.op == 'Const':
                continue
            possible_int8_res = [name for name in int8_op_prefix_list if i.op.find(name) != -1]

            if any(possible_int8_res):
                origin_op_type = possible_int8_res[0].split('Quantized')[-1]
                if origin_op_type == 'FusedBatchNorm':
                    origin_op_type = 'FusedBatchNormV3'
                if origin_op_type == 'FusedInstanceNorm':
                    origin_op_type = '_MklFusedInstanceNorm'
                if origin_op_type == 'Depthwise':
                    origin_op_type = 'DepthwiseConv2dNative'
                if origin_op_type == 'BatchMatMul':
                    origin_op_type = 'BatchMatMulV2'
                if origin_op_type == 'Deconv2D':
                    origin_op_type = 'Conv2DBackpropInput'
                if origin_op_type == 'Deconv3D':
                    origin_op_type = 'Conv3DBackpropInputV2'
                res[origin_op_type]['INT8'] += 1

            if i.op in fp32_op_list:
                if 'T' not in i.attr and i.op != 'Cast':
                    continue
                if i.attr['T'].type == dtypes.bfloat16:
                    res[i.op]['BF16'] += 1
                elif i.attr['T'].type in (dtypes.quint8,dtypes.qint8):
                    res[i.op]['INT8'] += 1
                elif i.op == 'Cast':
                    if i.attr['DstT'].type == dtypes.bfloat16:
                        res[i.op]['BF16'] += 1
                    elif i.attr['DstT'].type == dtypes.float32:
                        res[i.op]['FP32'] += 1
                else:
                    res[i.op]['FP32'] += 1
        
        field_names = ["Op Type", "Total", "INT8", "BF16", "FP32"]
        output_data = [[
            op_type, sum(res[op_type].values()), 
            res[op_type]['INT8'], res[op_type]['BF16'], res[op_type]['FP32']]
        for op_type in fp32_op_list]

        Statistics(output_data,
                   header='Mixed Precision Statistics',
                   field_names=field_names).print_stat()
        self.optype_statistics = field_names, output_data

    def _query_bf16_ops(self, matched_nodes):
        self.bf16_op_details = OrderedDict()

        valid_precision = self.query_handler.get_mixed_precision_combination()
        if ('bf16' in valid_precision and CpuInfo().bf16) or os.getenv('FORCE_BF16') == '1':
            for details in matched_nodes:
                node_op = details[-1][0]
                node_name = details[0]

                self.bf16_op_details[(node_name, node_op)] = [{'weight': {'dtype': ['bf16']}, \
                                                              'activation': {'dtype': ['bf16']}},\
                                                              {'weight': {'dtype': 'fp32'}, \
                                                               'activation': {'dtype': 'fp32'}}]

    def _query_quantizable_ops(self, matched_nodes):
        """Collect the op-wise configuration for quantization.

        Returns:
            OrderDict: op-wise configuration.
        """
        bf16_common_config = {'weight': {'dtype': 'bf16'}, 'activation': {'dtype': 'bf16'}}
        fp32_common_config = {'weight': {'dtype': 'fp32'}, 'activation': {'dtype': 'fp32'}}
        uint8_type = self.query_handler.get_op_types_by_precision(precision='uint8')
        int8_type = self.query_handler.get_op_types_by_precision(precision='int8')
        tf_quantizable_op_type = list(set(uint8_type).union(set(int8_type)))

        valid_precision = self.query_handler.get_mixed_precision_combination()
        op_capability = self.query_handler.get_quantization_capability()
        conv_config = copy.deepcopy(op_capability['uint8']['Conv2D'])
        conv3d_config = copy.deepcopy(op_capability['uint8']['Conv3D']) if 'Conv3D' in op_capability['uint8'] else None
        matmul_config = copy.deepcopy(op_capability['uint8']['MatMul'])
        other_config = copy.deepcopy(op_capability['uint8']['default'])
        
        self.quantizable_op_details = OrderedDict()

        self._init_op_stat = {i: [] for i in tf_quantizable_op_type}

        exclude_first_quantizable_op = True if 'first_conv_or_matmul_quantization' in \
                      self.recipes and not self.recipes['first_conv_or_matmul_quantization'] \
                      else False
        for details in matched_nodes:
            node_op = details[-1][0]
            node_name = details[0]
            patterns = details[-1]
            pat_length = len(patterns)
            pattern_info = {
                'sequence': [[','.join(patterns[:pat_length - i]) for i in range(pat_length)][0]],
                'precision': ['int8']
            }
            if node_op in tf_quantizable_op_type and node_name not in self.exclude_node_names and (
                node_name, self.unify_op_type_mapping[node_op]) not in self.quantizable_op_details:
                if exclude_first_quantizable_op and \
                    (self.unify_op_type_mapping[node_op].find("conv2d") != -1 or \
                    self.unify_op_type_mapping[node_op].find("matmul") != -1):
                    exclude_first_quantizable_op = False
                    self.exclude_node_names.append(node_name)
                    continue
                self._init_op_stat[node_op].append(node_name)
                if self.unify_op_type_mapping[node_op].find("conv2d") != -1:
                    conv2d_int8_config = copy.deepcopy(conv_config)
                    conv2d_int8_config['pattern'] = pattern_info
                    self.quantizable_op_details[(
                        node_name, self.unify_op_type_mapping[node_op]
                    )] = [conv2d_int8_config, fp32_common_config]
                elif self.unify_op_type_mapping[node_op].find("conv3d") != -1:
                    conv3d_int8_config = copy.deepcopy(conv3d_config)
                    conv3d_int8_config['pattern'] = pattern_info
                    self.quantizable_op_details[(
                        node_name, self.unify_op_type_mapping[node_op]
                    )] = [conv3d_int8_config, fp32_common_config]
                elif self.unify_op_type_mapping[node_op].find("matmul") != -1:
                    matmul_int8_config = copy.deepcopy(matmul_config)
                    matmul_int8_config['pattern'] = pattern_info
                    # TODO enable the sym mode once the tf fixed the mkldequantize_op.cc bug.
                    # is_positive_input = self.pre_optimizer_handle.has_positive_input(node_name)
                    # matmul_scheme = 'sym' if is_positive_input else 'asym'
                    matmul_scheme = ['asym']
                    matmul_int8_config['activation']['scheme'] = matmul_scheme
                    self.quantizable_op_details[(
                        node_name, self.unify_op_type_mapping[node_op]
                    )] = [matmul_int8_config, fp32_common_config]
                else:
                    self.quantizable_op_details[(
                        node_name, self.unify_op_type_mapping[node_op]
                    )] = [copy.deepcopy(other_config), fp32_common_config]
                if ('bf16' in valid_precision and CpuInfo().bf16) or os.getenv('FORCE_BF16') == '1':
                    self.quantizable_op_details[(
                        node_name, self.unify_op_type_mapping[node_op]
                    )].insert(1, bf16_common_config)

                self.quantize_config['op_wise_config'][node_name] = (False, "minmax", False)
        return self.quantizable_op_details

    def filter_unquantizable_concat(self, matched_nodes):
        target_concat_nodes = [i[0] for i in matched_nodes if i[-1][0] == 'ConcatV2']
        from neural_compressor.adaptor.tf_utils.util import GraphAnalyzer
        from neural_compressor.adaptor.tf_utils.graph_util import GraphRewriterHelper

        g = GraphAnalyzer()
        g.graph = self.pre_optimized_model.graph_def
        graph_info = g.parse_graph()
        concat_nodes = g.query_fusion_pattern_nodes([['ConcatV2']])
        for i in concat_nodes:
            concat_node_name = i[0]
            if concat_node_name not in target_concat_nodes:
                continue
            input_positive_status = []
            for index in range(graph_info[concat_node_name].node.attr['N'].i):
                each_input_name = GraphRewriterHelper.node_name_from_input(
                    graph_info[concat_node_name].node.input[index])
                each_input_node = graph_info[each_input_name].node
                positive_input = False
                if each_input_node.op in ('Relu', 'Relu6'):
                    positive_input = True
                else:
                    positive_input = g.has_positive_input(each_input_node.name)
                input_positive_status.append(positive_input)
            if not any(input_positive_status):
                matched_nodes.remove(i)

    def filter_unquantizable_concat_performance_only(self, matched_nodes):
        target_concat_nodes = [i[0] for i in matched_nodes if i[-1][0] == 'ConcatV2']
        from neural_compressor.adaptor.tf_utils.util import GraphAnalyzer
        from neural_compressor.adaptor.tf_utils.graph_util import GraphRewriterHelper

        g = GraphAnalyzer()
        g.graph = self.pre_optimized_model.graph_def
        graph_info = g.parse_graph()
        concat_nodes = g.query_fusion_pattern_nodes([['ConcatV2']])
        for i in concat_nodes:
            concat_node_name = i[0]
            if concat_node_name not in target_concat_nodes:
                continue
            input_positive_status = []
            control_flow = False
            for index in range(graph_info[concat_node_name].node.attr['N'].i):
                each_input_name = GraphRewriterHelper.node_name_from_input(
                    graph_info[concat_node_name].node.input[index])
                each_input_node = graph_info[each_input_name].node
                if each_input_node.op in ('Switch'):
                    control_flow  = True
            if control_flow:
                matched_nodes.remove(i)

    def query_fw_capability(self, model):
        """Collect the model-wise and op-wise configuration for quantization.

        Args:
            model (tf.compat.v1.GraphDef): model definition.

        Returns:
            [dict]: model-wise & op-wise configuration for quantization.
        """
        from .tf_utils.graph_rewriter.generic.pre_optimize import PreOptimization

        self.pre_optimizer_handle = PreOptimization(model, self.optimization, self.new_api, self.device)

        self.pre_optimized_model = self.pre_optimizer_handle.get_optimized_model(self.itex_mode)
        model.graph_def = self.pre_optimized_model.graph_def

        self.exclude_node_names = self.pre_optimizer_handle.get_excluded_node_names()
        patterns = self.query_handler.generate_internal_patterns()
        bf16_patterns = self.query_handler.get_bf16_patterns()
        matched_nodes = self.pre_optimizer_handle.get_matched_nodes(patterns)
        matched_bf16_nodes = self.pre_optimizer_handle.get_matched_nodes(bf16_patterns)
        original_graph_node_name = [i.name for i in model.graph_def.node]
        matched_nodes = sorted(matched_nodes, reverse=True, key=lambda i: (
            original_graph_node_name.index(i[0]), len(i[-1])))

        def check_match(patterns, input_pattern):
            for i in patterns:
                if input_pattern == [i for i in i.replace('+', ' ').strip().split(' ') if i]:
                    return True
            return False


        if self.new_api and self.performance_only:
            self.filter_unquantizable_concat_performance_only(matched_nodes)
        else:
            self.filter_unquantizable_concat(matched_nodes)

        copied_matched_nodes = copy.deepcopy(matched_nodes)
        for i in copied_matched_nodes:
            if i[-1][0] in self.query_handler.get_op_types()['int8']:
                continue

            if not self.pre_optimizer_handle.has_positive_input(i[0]) and \
                not check_match(self.query_handler.get_fuse_patterns()['int8'], i[-1]):
                matched_nodes.remove(i)

        del copied_matched_nodes

        copied_matched_nodes = copy.deepcopy(matched_bf16_nodes)
        for i in copied_matched_nodes:
            for j in matched_nodes:
                if i[0] == j[0] and i in matched_bf16_nodes:
                    matched_bf16_nodes.remove(i)

        del copied_matched_nodes

        self._query_quantizable_ops(matched_nodes)
        self._query_bf16_ops(matched_bf16_nodes)
        capability = {
            'optypewise': self.get_optype_wise_ability(),
        }
        capability['opwise'] = copy.deepcopy(self.quantizable_op_details)
        capability['opwise'].update(self.bf16_op_details)
        logger.debug("Dump framework quantization capability:")
        logger.debug(capability)

        return capability

    def set_tensor(self, model, tensor_dict):
        from .tf_utils.graph_util import GraphAnalyzer
        g = GraphAnalyzer()
        g.graph = model.graph_def
        graph_info = g.parse_graph()

        def _get_fp32_op_name(model, tensor_name):
            is_weight = False
            is_biasadd = False
            last_node_name = None
            current_node_name = None
            for each_node in model.graph_def.node:

                if tensor_name in each_node.input:
                    tensor_index = list(each_node.input).index(tensor_name)
                    if each_node.op.find("Quantized") != -1 and tensor_index == 2:
                        is_biasadd = True
                        last_node_name = each_node.input[0]
                        current_node_name = each_node.name

                if tensor_name + "_qint8_const" in each_node.input:
                    pass

            return is_weight, is_biasadd, current_node_name, last_node_name

        from neural_compressor.adaptor.tf_utils.graph_util import GraphRewriterHelper as Helper
        from tensorflow.python.framework import dtypes
        from tensorflow.python.framework import tensor_util
        from tensorflow.core.framework import attr_value_pb2
        qint32_type = dtypes.qint32.as_datatype_enum

        for tensor_name, tensor_content in tensor_dict.items():
            is_weight, is_biasadd, current_node_name, last_node_name = \
                    _get_fp32_op_name(model, tensor_name)

            if is_biasadd:
                is_biasadd_dtype_is_fp32 = graph_info[\
                        current_node_name].node.attr['Tbias'] == attr_value_pb2.AttrValue(
                    type=dtypes.float32.as_datatype_enum)
                current_node = graph_info[current_node_name].node
                bias_add_node = graph_info[current_node.input[2]].node
                if is_biasadd_dtype_is_fp32:
                    bias_add_node.attr["value"].CopyFrom(
                        attr_value_pb2.AttrValue(
                            tensor=tensor_util.make_tensor_proto(tensor_content,
                            dtypes.float32, tensor_content.shape)))
                else:
                    last_node = graph_info[last_node_name].node
                    min_input = graph_info[\
                            last_node.input[-2]].node.attr['value'].tensor.float_val[0]
                    max_input = graph_info[\
                            last_node.input[-1]].node.attr['value'].tensor.float_val[0]
                    channel_size = tensor_content.shape[0]
                    max_filter_node = graph_info[current_node.input[6]].node
                    min_filter_node = graph_info[current_node.input[5]].node
                    if max_filter_node.attr['value'].tensor.float_val:
                        max_filter_tensor = []
                        min_filter_tensor = []
                        max_filter_tensor.append(\
                                (max_filter_node.attr['value'].tensor.float_val)[0])
                        min_filter_tensor.append(\
                                (min_filter_node.attr['value'].tensor.float_val)[0])
                    else:
                        max_filter_tensor = tensor_util.MakeNdarray(\
                                min_filter_node.attr['value'].tensor)
                        min_filter_tensor = tensor_util.MakeNdarray(\
                                min_filter_node.attr['value'].tensor)
                    activation_range = 127.0 if \
                            current_node.attr["Tinput"].type == dtypes.qint8 else 255.0
                    updated_bias = Helper.generate_int32_bias_for_conv(\
                            tensor_content, channel_size, max_input, min_input, \
                                max_filter_tensor, min_filter_tensor, activation_range)

                    bias_add_node.attr['dtype'].CopyFrom(\
                            attr_value_pb2.AttrValue(type=qint32_type))
                    bias_add_node.attr["value"].CopyFrom(\
                        attr_value_pb2.AttrValue(
                            tensor=tensor_util.make_tensor_proto(updated_bias,
                            dtypes.int32, tensor_content.shape)))
                    bias_add_node.attr['value'].tensor.dtype = qint32_type
                    current_node.attr["Tbias"].CopyFrom(attr_value_pb2.AttrValue(type=qint32_type))

            if is_weight:
                tmp_const_node = Helper.create_constant_node(\
                        current_node.name + '_weights_tmp',
                        tensor_content.transpose(2,3,1,0), dtypes.float32)
                min_filter_node = graph_info[current_node.input[5]].node
                per_channel = True if min_filter_node.attr['value'].tensor.tensor_shape else False
                from .tf_utils.quantize_graph_common import QuantizeGraphHelper
                original_fp32_op = current_node.op.split("With")[0].split("Quantized")[-1]
                if original_fp32_op.find("Depthwise") != -1:
                    original_fp32_op = "DepthwiseConv2dNative"
                qint8_const_node, min_node, max_node = \
                        QuantizeGraphHelper.generate_quantized_weight_node(
                            original_fp32_op, tmp_const_node, per_channel)
                g.add_node(qint8_const_node, [], [current_node.name])
                g.add_node(min_node, [], [current_node.name])
                g.add_node(max_node, [], [current_node.name])
                g.replace_constant_graph_with_constant_node(qint8_const_node, tensor_name)
                g.replace_constant_graph_with_constant_node(min_node, current_node.input[5])
                g.replace_constant_graph_with_constant_node(max_node, current_node.input[6])

    def inspect_weight_and_bias(self, node_list, graph_def, graph_info, graph_node_name_mapping):
        """
        Inspect the weights
        """
        from neural_compressor.utils.utility import DequantizeWeight
        from neural_compressor.adaptor.tf_utils.util import get_tensor_val_from_graph_node
        from .tf_utils.util import int8_node_name_reverse
        import tensorflow as tf
        weights_result = {}
        inspect_nodes = []
        node_set = set(node_list)
        for node in graph_def.node:
            node_name = node.name
            if 'Quantized' in node.op:
                node_name = int8_node_name_reverse(node)
            if node_name in node_set and ('Conv' in node.op or 'Mul' in node.op):
                inspect_nodes.append(node)
        logger.debug(f'Start to inspect weight and bias for: {[node.name for node in inspect_nodes]}.')
        for node in inspect_nodes:
            # inspect weights and bias
            node_name = node.name
            weight_node_name = node.input[1]
            weight_node = graph_node_name_mapping[weight_node_name]
            if weight_node.op != 'Const': # skip the matmul whose two inputs are previous output
                continue
            weight_node_val = get_tensor_val_from_graph_node(graph_node_name_mapping, weight_node_name)
            weight_node_val = weight_node_val.astype('float32')
            # dequantize the weight for quantized model
            if 'Quantized' in node.op:
                node_name = int8_node_name_reverse(node)
                weight_node_name_pre = weight_node_name.split('_qint8_const')[0]
                min_filter_node = weight_node_name_pre + '_min'
                max_filter_node = weight_node_name_pre + '_max'
                if graph_info[min_filter_node].node.attr['value'].tensor.float_val:
                    min_filter_val = graph_info[min_filter_node].node.attr['value'].tensor.float_val
                    max_filter_val = graph_info[max_filter_node].node.attr['value'].tensor.float_val
                else:
                    min_filter_val = get_tensor_val_from_graph_node(graph_node_name_mapping, min_filter_node)
                    max_filter_val = get_tensor_val_from_graph_node(graph_node_name_mapping, max_filter_node)
                DequantizeWeight(weight_node_val, min_filter_val, max_filter_val)
            weights_result[node_name] = {weight_node_name: weight_node_val}
            
            # get bias from quantized model directly
            if 'Quantized' in node.op:
                if 'Bias' in node.op:
                    bias_node_name = node.input[2]
                    bias_val = get_tensor_val_from_graph_node(graph_node_name_mapping, bias_node_name)
                    weights_result[node_name][bias_node_name] = bias_val.astype('float32')
            # get bias from fp32 model
            else:
                bias_add_node = None
                if graph_info[node.name].outputs:
                    bias_add_node = graph_info[graph_info[node.name].outputs[0]].node
                if bias_add_node and bias_add_node.op == 'BiasAdd':
                    bias_node_name = bias_add_node.input[1]
                    bias_node_val = get_tensor_val_from_graph_node(graph_node_name_mapping, bias_node_name)
                    weights_result[node_name][bias_node_name] = bias_node_val
        return weights_result

    def fused_node_mapping(self, node_list, pattern_mapping, graph_info, graph_node_name_mapping):
        """
        Create the mapping between first node and last node in fused sequence
        Args:
            node_list: node name list
            pattern_mapping:  key: node name, val: node pattern mapping
            graph_info: key: node name, val: node details
            graph_node_name_mapping: key: node name, val: node
        Returns:
            fused_mapping: key: first node name in fused seq, val: last node in fused seq
            fused_mapping_reverse: key: last node in fused seq, val: first node name in fused seq
        """
        fused_mapping = {}
        fused_mapping_reverse = {}
        for node_name in node_list:
            fused_seq = pattern_mapping[node_name]['sequence'].split(',')
            # for the node not fused with others
            if len(fused_seq) == 1:
                fused_mapping[node_name] = node_name
                fused_mapping_reverse[node_name] = node_name
                continue
            _next_node_name = node_name
            for _next_node_op_type in fused_seq[1:]:
                node_details = graph_info[_next_node_name]
                for node_output_name in node_details.outputs:
                    if graph_node_name_mapping[node_output_name].op == 'Cast':
                        cast_node = graph_node_name_mapping[node_output_name]
                        node_output_name = graph_info[cast_node.name].outputs[0]
                    if graph_node_name_mapping[node_output_name].op in [_next_node_op_type, 'Cast']:
                        _next_node_name = node_output_name
            fused_mapping[node_name] = _next_node_name
            fused_mapping_reverse[_next_node_name] = node_name
        return fused_mapping, fused_mapping_reverse

    def _inspect_tensor_inference(self, inspect_node_dict,  model, dataloader, iteration_list):
        """
        Do inference for inspect activation
        """
        out_tensor_lst = []
        out_tensor_lst += [{n : [n + ':' + str(i) for i in range(3)]} for n in inspect_node_dict['qreq_node']]
        out_tensor_lst += [{n : n + ':0'} for n in inspect_node_dict['qdq_node']]
        out_tensor_lst += [{n : n + ':0'} for n in inspect_node_dict['f_node']]
        out_cnt = len(out_tensor_lst)
        iteration_list = set(iteration_list)
        input_tensor = model.input_tensor
        logger.info('Start to do inference for inspect activation.')
        activation_result = []
        for idx, (inputs, labels) in enumerate(dataloader):
            model_out = []
            if idx + 1 > max(iteration_list):
                break
            if idx + 1 not in iteration_list:
                continue
            if len(input_tensor) == 1:
                feed_dict = {input_tensor[0]: inputs}  # get raw tensor using index [0]
            else:
                assert len(input_tensor) == len(inputs), \
                    'inputs len must equal with input_tensor'
                feed_dict = dict(zip(input_tensor, inputs))
            #TODO find an optimized method to avoid multiple runs
            for i, out_t in enumerate(out_tensor_lst):
                logger.debug(f'Finished inspect {i}/{out_cnt} nodes, current inspect node {out_t.keys()}.')
                model_out.append(model.sess.run(out_t, feed_dict))
            activation_result.append(model_out)
        return activation_result

    def inspect_activation(self, node_list, graph_def, graph_node_name_mapping, quantization_cfg,
                           dataloader, iteration_list, graph_info):
        """
        Inspect the activation.
        """
        from neural_compressor.experimental.common import Model
        original_graph_node_mapping = {}
        for node in graph_def.node:
            original_graph_node_mapping[node.name] = node
        inspect_node_dict = {'qdq_node':[], 'qreq_node':[], 'f_node':[]}
        for node_name in node_list:
            node = graph_node_name_mapping[node_name]
            if 'Quantized' in node.op and 'Dequantize' in node.op:
                inspect_node_dict['qdq_node'].append(node.name)
            elif 'Quantized' in node.op or '_Quantized' in node.op or 'Requantize' in node.op:
                inspect_node_dict['qreq_node'].append(node.name)
            else:
                inspect_node_dict['f_node'].append(node_name)
        pattern_mapping = {}  
        node_dict = quantization_cfg['op']
        for node_name_and_type in node_dict.keys():
            node_name, _ = node_name_and_type
            if 'pattern' in node_dict[node_name_and_type]:
                pattern_mapping[node_name] = node_dict[node_name_and_type]['pattern']
            else:
                pattern_mapping[node_name] = {'sequence': node_name}
        if inspect_node_dict['f_node']:
            fuse_map, fuse_map_reverse = self.fused_node_mapping(inspect_node_dict['f_node'], pattern_mapping, 
                                                                 graph_info, graph_node_name_mapping)
            inspect_node_dict['f_node'] = [fuse_map[n] for n in inspect_node_dict['f_node']]
        # build model and do inference
        model = Model(graph_def)
        activation_result = self._inspect_tensor_inference(inspect_node_dict, model, dataloader, iteration_list)
        final_result = []
        int8_postfix = '_eightbit'
        for iter_res in activation_result:
            tmp_iter_result = {}
            for res in iter_res:
                node_name, val = list(res.keys())[0], list(res.values())[0]
                val = Dequantize(val[0], (node_name, val[1], val[2])) if len(val) == 3 else val
                index_postfix = node_name.find(int8_postfix)
                if index_postfix != -1:
                    node_name = node_name[:index_postfix]
                    tmp_iter_result[node_name] = {node_name: val}
                else:
                    tmp_iter_result[fuse_map_reverse[node_name]] = {fuse_map_reverse[node_name]: val}
            final_result.append(tmp_iter_result)
        return final_result

    def inspect_tensor(self, model, dataloader=None, op_list=[], iteration_list=[],
                       inspect_type='activation', save_to_disk=False, save_path=None, quantization_cfg=None):
        """
        Dump the weight and activation(output) to local disk.
        1. create the correspondence between query node name and the actually output node name in graph_def
        2. get the weight and bias for the given node
        3. get the activation for the given node
        4. save the tensor to disk
        Args:
            model: int8/fp32 graph_def/TensorflowBaseModel
            dataloader: dataloader used during inspect activation
            op_list: op list to inspect
            iteration_list: iteration list to inspect, start from 1
            inspect_type: activation/weight/all
            save_to_disk: dump to disk or not
            save_path: the dump path for inspect tensor
            quantization_cfg: quantization configuration for fused fp32 model and quantized model
        Returns:
            Dict
               {
                 'weight': {
                   'node0_name': {'weight0_name': numpy.array, 'bias0_name': numpy.array, ...},
                   'node1_name': {'weight1_name': numpy.array, 'bias1_name': numpy.array, ...},
                   ...
                 },
                 'activation': [
                   # iter 1:
                       {
                         'node0_name': {'output0_name': numpy.array, 'output1_name': numpy.array, ...}
                         'node1_name': {'output1_name': numpy.array, 'output1_name': numpy.array, ...}
                         ...
                       },
                   # iter 2:
                        {
                       ...
                       }
                 ]
               }
        """
        from neural_compressor.model.model import TensorflowBaseModel
        from neural_compressor.utils.utility import load_data_from_pkl, dump_data_to_local
        from neural_compressor.adaptor.tf_utils.graph_util import GraphAnalyzer
        from .tf_utils.util import int8_node_name_reverse
        import tensorflow as tf
        if isinstance(model, TensorflowBaseModel):
            model = model.graph_def
        if not quantization_cfg:
            # TODO get config from graph if config is None
            quantization_cfg = load_data_from_pkl('./nc_workspace/', 'cfg.pkl')
        node_list = op_list
        # create the mapping between node name and node, key: node_name, val: node
        graph_node_name_mapping = {}
        quan_model_flag = False
        for node in model.node:
            node_name = int8_node_name_reverse(node)
            if 'Quantized' in node.op:
                quan_model_flag = True
                node_name = int8_node_name_reverse(node)
            if node.attr['value'].tensor.dtype == tf.dtypes.bfloat16.as_datatype_enum:
                quan_model_flag = True
            graph_node_name_mapping[node_name] = node
        if quan_model_flag:
            logger.info('Dump the tensor for quantized model.')

        # create the mapping between node name and node detail
        g = GraphAnalyzer()
        g.graph = model
        graph_info = g.parse_graph()
        inspect_result = {}
        
        # inspect weight
        if inspect_type == 'weight' or inspect_type == 'all':
            logger.info('Start to inspect weight and bias.')
            weights_result = self.inspect_weight_and_bias(node_list, model, graph_info, graph_node_name_mapping)
            inspect_result['weight'] = weights_result
            
        # inspect activation
        if inspect_type == 'activation' or inspect_type == 'all':
            logger.info('Start to inspect activation.')
            activation_result = self.inspect_activation(node_list, model, graph_node_name_mapping, quantization_cfg,
                                                        dataloader, iteration_list, graph_info)
            inspect_result['activation'] = activation_result

        # save to disk
        if save_to_disk:
            if not save_path:
                save_path = './nc_workspace/tmp/'
            dump_data_to_local(inspect_result, save_path, 'inspect_result.pkl')
            logger.info(f'Dumped the inspect tensor to {save_path}')
        return inspect_result


    def quantize_input(self, model):
        ''' quantize the model to be able to take quantized input
            remove graph QuantizedV2 op and move its input tensor to QuantizedConv2d
            and calculate the min-max scale

            Args:
                model (tf.compat.v1.GraphDef): The model to quantize input

            Return:
                model (tf.compat.v1.GraphDef): The quantized input model
                scale (float): The scale for dataloader to generate quantized input
        '''
        scale = None
        # quantize input only support tensorflow version > 2.1.0
        import tensorflow as tf
        if version1_lt_version2(tf.version.VERSION, '2.1.0'):
            logger.warning("Quantize input needs tensorflow 2.1.0 and newer.")
            return model, scale

        graph_def = model.as_graph_def()
        node_name_mapping = {}
        quantize_nodes = []
        for node in graph_def.node:
            node_name_mapping[node.name] = node
            if node.op == 'QuantizeV2':
                quantize_nodes.append(node)

        target_quantize_nodes = []
        for node in quantize_nodes:
            # only support Quantizev2 input op Pad and Placeholder
            if (node_name_mapping[node.input[0]].op == 'Pad' and node_name_mapping[
                    node_name_mapping[node.input[0]].input[0]].op == 'Placeholder') or \
                    node_name_mapping[node.input[0]].op == 'Placeholder':
                target_quantize_nodes.append(node)
        assert len(target_quantize_nodes) == 1, 'only support 1 QuantizeV2 from Placeholder'
        quantize_node = target_quantize_nodes[0]

        quantize_node_input = node_name_mapping[quantize_node.input[0]]
        quantize_node_outputs = [node for node in graph_def.node
                                 if quantize_node.name in node.input]

        from .tf_utils.graph_util import GraphRewriterHelper
        if quantize_node_input.op == 'Pad':
            pad_node_input = node_name_mapping[quantize_node_input.input[0]]
            assert pad_node_input.op == 'Placeholder', \
                'only support Pad between QuantizeV2 and Placeholder'
            from tensorflow.python.framework import tensor_util
            paddings_tensor = tensor_util.MakeNdarray(node_name_mapping[
                quantize_node_input.input[1]].attr['value'].tensor).flatten()

            quantize_node.input[0] = quantize_node_input.input[0]
            for conv_node in quantize_node_outputs:
                assert 'Conv2D' in conv_node.op, 'only support QuantizeV2 to Conv2D'

                GraphRewriterHelper.set_attr_int_list(conv_node,
                                                      "padding_list", paddings_tensor)
            graph_def.node.remove(quantize_node_input)

        from tensorflow.python.framework import dtypes
        GraphRewriterHelper.set_attr_dtype(node_name_mapping[quantize_node.input[0]],
                                           "dtype", dtypes.qint8)

        for conv_node in quantize_node_outputs:
            for index, conv_input in enumerate(conv_node.input):
                if conv_input == quantize_node.name:
                    conv_node.input[index] = quantize_node.input[0]
                elif conv_input == quantize_node.name + ":1":
                    conv_node.input[index] = quantize_node.input[1]
                elif conv_input == quantize_node.name + ":2":
                    conv_node.input[index] = quantize_node.input[2]

        # get the input's min-max value and calculate scale
        max_node = node_name_mapping[quantize_node.input[2]]
        min_node = node_name_mapping[quantize_node.input[1]]
        max_value = max_node.attr['value'].tensor.float_val[0]
        min_value = min_node.attr['value'].tensor.float_val[0]
        scale = 127. / max(abs(max_value), abs(min_value))
        # remove QuantizeV2 node
        graph_def.node.remove(quantize_node)

        graph = tensorflow.Graph()
        with graph.as_default():
            # use name='' to avoid 'import/' to name scope
            tensorflow.import_graph_def(graph_def, name='')
        return graph, scale

    def get_optype_wise_ability(self):
        """Get the op type wise capability by generating the union value of each op type.
        Returns:
            [string dict]: the key is op type while the value is the
                           detail configurations of activation and weight for this op type.
        """
        res = OrderedDict()
        for op in self.quantizable_op_details:
            if op[1] not in res:
                    res[op[1]] = {'activation': self.quantizable_op_details[op][0]['activation']}
                    if 'weight' in self.quantizable_op_details[op][0]:
                        res[op[1]]['weight'] = self.quantizable_op_details[op][0]['weight']
        for op in self.bf16_op_details:
            if op[1] not in res:
                res[op[1]] = {'activation': {'dtype': ['bf16']}, 'weight': {'dtype': ['bf16']}}
        return res

    def _pre_eval_hook(self, model):
        return model

    # Add keyword arguments unpacking
    def _post_eval_hook(self, model, **kwargs):
        pass

    def save(self, model, path):
        pass

    def convert(self, model, source, destination):
        '''The function is used to convert a source model format to another.

           Args:
               model (neural_compressor.model): base model to be converted.
               source (string): The source model format.
               destination (string): The destination model format.
        '''
        assert source.lower() == 'qat' and destination.lower() == 'default'
        capability = self.query_fw_capability(model)

        quantize_config = {'op_wise_config': {}}
        for each_op_info in capability['opwise']:
            is_perchannel = False
            weight_bit = 7.0
            for op_cap in capability['opwise'][each_op_info]:
                if'activation'in op_cap and 'quant_mode' in op_cap['activation']:
                    activation = op_cap['activation']
                    if 'weight' in op_cap:
                        weight = op_cap['weight']
                        is_perchannel = True if weight[
                            'granularity'][0] == 'per_channel' else False
                    algorithm = activation['algorithm'][0]
                    is_asymmetric = False
                    if 'activation' in op_cap:
                        is_asymmetric = True if activation['scheme'][0] == 'asym' else False

                    quantize_config['op_wise_config'][each_op_info[0]] = (is_perchannel,
                                                                          algorithm,
                                                                          is_asymmetric,
                                                                          weight_bit)
        from .tf_utils.graph_converter import GraphConverter
        tmp_graphdef = copy.deepcopy(model.graph_def)
        for i in tmp_graphdef.node:
            if i.op == 'Const' and i.input:
                i.ClearField('input')
        model.graph_def = tmp_graphdef
        converter = GraphConverter(model,
                                   qt_config=quantize_config,
                                   int8_sequences=self.op_wise_sequences,
                                   fake_quant=True, new_api=self.new_api,
                                   performance_only = self.performance_only)

        return converter.convert()

    @dump_elapsed_time("Pass recover model")
    def recover_tuned_model(self, model, q_config):
        """Execute the recover process on the specified model.

            Args:
                tune_cfg (dict): quantization configuration
                model (tf.compat.v1.GraphDef): fp32 model
                q_config (dict): recover configuration

            Returns:
                tf.compat.v1.GraphDef: the quantized model
        """
        from .tf_utils.graph_rewriter.generic.pre_optimize import PreOptimization
        self.pre_optimizer_handle = PreOptimization(model, self.optimization, self.new_api, self.device)
        self.pre_optimized_model = self.pre_optimizer_handle.get_optimized_model(self.itex_mode)
        model.graph_def = self.pre_optimized_model.graph_def

        from .tf_utils.graph_converter_without_calib import GraphConverterWithoutCalib
        converter = GraphConverterWithoutCalib(model,
                                            recover_config=q_config,
                                            new_api=self.new_api,
                                            performance_only=self.performance_only)

        return converter.convert_without_calib()
    
    def diagnosis_helper(self, fp32_model, quan_model, tune_cfg, save_path):
        from .tf_utils.util import tf_diagnosis_helper
        return tf_diagnosis_helper(fp32_model, quan_model, tune_cfg, save_path)


@adaptor_registry
class Tensorflow_ITEXAdaptor(TensorFlowAdaptor):
    def __init__(self, framework_specific_info):
        super().__init__(framework_specific_info)

    @dump_elapsed_time("Pass quantize model")
    def quantize(self, tune_cfg, model, data_loader, q_func=None):
        """Execute the quantize process on the specified model.

        Args:
            tune_cfg (dict): quantization configuration
            model (tf.compat.v1.GraphDef): fp32 model
            data_loader (generator): generator the data and labels
            q_func (optional): training function for quantization aware training mode,
                                which not enabled for tensorflow yet.

        Returns:
            tf.compat.v1.GraphDef: the quantized model
        """
        assert q_func is None, "quantization aware training mode is not support on tensorflow"
        self.tuning_cfg_to_fw(tune_cfg)
        logger.debug('Dump quantization configurations:')
        logger.debug(self.quantize_config)
        from .tf_utils.graph_converter import GraphConverter
        calib_sampling_size = tune_cfg.get('calib_sampling_size', 1)
        if isinstance(data_loader, BaseDataLoader):
            batch_size = data_loader.batch_size
            try:
                for i in range(batch_size):
                    if calib_sampling_size % (batch_size - i) == 0:
                        calib_batch_size = batch_size - i
                        if i != 0:  # pragma: no cover
                            logger.warning("Reset `calibration.dataloader.batch_size` field "
                                           "to {}".format(calib_batch_size) +
                                           " to make sure the sampling_size is "
                                           "divisible exactly by batch size")
                        break
                tmp_iterations = int(math.ceil(calib_sampling_size / calib_batch_size))
                data_loader.batch(calib_batch_size)
                self.quantize_config['calib_iteration'] = tmp_iterations
                converted_model = GraphConverter(model,
                                    qt_config=self.quantize_config,
                                    recipes=self.recipes,
                                    int8_sequences=self.op_wise_sequences,
                                    fp32_ops=self.fp32_ops,
                                    bf16_ops=self.bf16_ops,
                                    data_loader=data_loader,
                                    itex_mode=self.itex_mode,
                                    qdq_enabled=self.qdq_enabled,
                                    new_api=self.new_api,
                                    performance_only = self.performance_only).convert()
            except Exception: # pragma: no cover
                logger.warning(
                        "Fail to forward with batch size={}, set to {} now.".
                        format(batch_size, 1))
                data_loader.batch(1)
                self.quantize_config['calib_iteration'] = calib_sampling_size
                converted_model = GraphConverter(model,
                                qt_config=self.quantize_config,
                                recipes=self.recipes,
                                int8_sequences=self.op_wise_sequences,
                                fp32_ops=self.fp32_ops,
                                bf16_ops=self.bf16_ops,
                                data_loader=data_loader,
                                itex_mode=self.itex_mode,
                                qdq_enabled=self.qdq_enabled,
                                new_api=self.new_api,
                                performance_only = self.performance_only).convert()
        else: # pragma: no cover
            if hasattr(data_loader, 'batch_size') and \
              calib_sampling_size % data_loader.batch_size != 0:
                iter = self.quantize_config['calib_iteration']
                logger.warning(
                    "Please note that calibration sampling size {} " \
                    "isn't divisible exactly by batch size {}. " \
                    "So the real sampling size is {}.".
                    format(calib_sampling_size, data_loader.batch_size,
                           data_loader.batch_size * iter))
            converted_model = GraphConverter(model,
                                   qt_config=self.quantize_config,
                                   recipes=self.recipes,
                                   int8_sequences=self.op_wise_sequences,
                                   fp32_ops=self.fp32_ops,
                                   bf16_ops=self.bf16_ops,
                                   data_loader=data_loader,
                                   itex_mode=self.itex_mode,
                                   qdq_enabled=self.qdq_enabled,
                                   new_api=self.new_api,
                                   performance_only = self.performance_only).convert()

        self._dump_model_op_stats(converted_model.graph_def)

        return converted_model

class TensorflowQuery(QueryBackendCapability):

    def __init__(self, local_config_file=None, performance_only=False):
        import tensorflow as tf

        super().__init__()
        self.version = tf.version.VERSION
        self.cfg = local_config_file
        self.cur_config = None
        self.performance_only = performance_only
        self._one_shot_query()

    def _get_specified_version_cfg(self, data):
        """Get the configuration for the current runtime.
        If there's no matched configuration in the input yaml, we'll
        use the configuration of the nearest framework version field of yaml.

        Args:
            data (Yaml content): input yaml file.

        Returns:
            [dictionary]: the content for specific version.
        """
        from functools import cmp_to_key
        from pkg_resources import parse_version
        config = None

        def _compare(version1, version2):
            if parse_version(version1) == parse_version(version2):
                return 0
            elif parse_version(version1) < parse_version(version2):
                return -1
            else:
                return 1

        fallback_list = []
        for sub_data in data:
            if 'default' in sub_data['version']['name']:
                assert config == None, "Only one default config " \
                       "is allowed in framework yaml file."
                config = sub_data

            if self.version in sub_data['version']['name']:
                return sub_data
            else:
                sorted_list = copy.deepcopy(sub_data['version']['name'])
                sorted_list.remove('default') if 'default' in sorted_list else None
                if isinstance(sorted_list, list):
                    # TensorFlow 1.15.0-up1/up2/up3 release versions are abnoraml release naming
                    # convention. Replacing them with dot for version comparision.
                    sorted_list = [i.replace('-up', '.') for i in sorted_list]
                    sorted_list = sorted(sorted_list, key=cmp_to_key(_compare), reverse=True)
                else:
                    assert isinstance(sorted_list, str)
                    sorted_list = list(sorted_list.replace('-up', '.').split())
                for i in sorted_list:
                    if parse_version(self.version) >= parse_version(i):
                        fallback_list.append([i, sub_data])
                        break

        assert config != None, "The default config in framework yaml must exist."
        nearest_version = str(0)
        for fallback in fallback_list:
            if parse_version(fallback[0]) > parse_version(nearest_version):
                nearest_version = fallback[0]
                config = fallback[1]

        return config

    def _one_shot_query(self):
        # pylint: disable=E1136
        with open(self.cfg) as f:
            content = yaml.safe_load(f)
            try:
                self.cur_config = self._get_specified_version_cfg(content)
                if not self.performance_only:
                    remove_int8_ops = ['FusedBatchNorm', 'FusedBatchNormV2', 'FusedBatchNormV3',
                                       '_MklFusedInstanceNorm']
                    for op in remove_int8_ops:
                        while op in self.cur_config['ops']['int8']:
                            self.cur_config['ops']['int8'].remove(op)
                        if self.cur_config.get('capabilities'):
                            self.cur_config['capabilities']['int8'].pop(op, None)
                        patterns = [f'Dequantize + {op} + Relu + QuantizeV2',
                                    f'Dequantize + {op} + LeakyRelu + QuantizeV2']
                        for pattern in patterns:
                            if self.cur_config.get('patterns'):
                                while pattern in self.cur_config['patterns']['int8']:
                                    self.cur_config['patterns']['int8'].remove(pattern)

            except Exception as e:
                logger.info("Fail to parse {} due to {}.".format(self.cfg, str(e)))
                self.cur_config = None
                raise ValueError("Please check if the format of {} follows Neural Compressor yaml schema.".
                                 format(self.cfg))
        self._update_cfg_with_usr_definition()

    def _update_cfg_with_usr_definition(self):
        from neural_compressor.conf.pythonic_config import tensorflow_config
        if tensorflow_config.precisions is not None:
            self.cur_config['precisions']['names'] = ','.join(tensorflow_config.precisions)

    def get_version(self):
        """Get the current backend version infomation.

        Returns:
            [string]: version string.
        """
        return self.cur_config['version']['name']

    def get_precisions(self):
        """Get supported precisions for current backend.

        Returns:
            [string list]: the precisions' name.
        """
        return self.cur_config['precisions']['names']

    def get_op_types(self):
        """Get the supported op types by all precisions.

        Returns:
            [dictionary list]: A list composed of dictionary which key is precision
            and value is the op types.
        """
        return self.cur_config['ops']

    def get_fuse_patterns(self):
        """Get supported patterns by low precisions.

        Returns:
            [dictionary list]: A list composed of dictionary which key is precision
            and value is the supported patterns.
        """
        return self.cur_config['patterns']

    def get_quantization_capability(self):
        """Get the supported op types' quantization capability.

        Returns:
            [dictionary list]: A list composed of dictionary which key is precision
            and value is a dict that describes all op types' quantization capability.
        """
        return self.cur_config['capabilities']

    def get_op_types_by_precision(self, precision):
        """Get op types per precision

        Args:
            precision (string): precision name

        Returns:
            [string list]: A list composed of op type.
        """
        assert precision in list(self.cur_config['ops'].keys())

        return self.cur_config['ops'][precision]

    def get_mixed_precision_combination(self):
        """Get the valid mixed precisions.

        Returns:
            [string list]: valid precision list.
        """
        if self.cur_config['precisions']['valid_mixed_precisions']:
            return [i.strip() for i in self.cur_config['precisions']['valid_mixed_precisions']]

        return [i.strip() for i in self.get_precisions().split(',')]

    def get_grappler_optimization_cfg(self):
        return self.cur_config['grappler_optimization']

    def get_bf16_patterns(self):
        #int8_op_types = self.get_op_types_by_precision('int8') + self.get_op_types_by_precision('uint8')
        bf16_op_types = [i for i in self.get_op_types_by_precision('bf16')]
        #bf16_op_types = [i for i in self.get_op_types_by_precision('bf16') if i not in int8_op_types]
        res = []
        for i in bf16_op_types:
            res.append([[i]])

        return res

    def get_eightbit_patterns(self, qdq_enabled=False):
        """Get eightbit op wise sequences information.

        Returns:
            [dictionary]: key is the op type while value is the list of sequences start
                        with the op type same as key value.
        """
        quantizable_op_types = self.get_op_types_by_precision(
            'int8') + self.get_op_types_by_precision('uint8')
        int8_patterns = [i.replace(
            '+', ' ').split() for i in list(set(self.get_fuse_patterns()['int8'] +
                                                self.get_fuse_patterns()['uint8']))]

        res = {}
        for i in quantizable_op_types:
            if qdq_enabled:
                res[i] = [['Dequantize', i, 'QuantizeV2']]
            else:
                res[i] = [[i]]
               
        
        for pattern in int8_patterns:
            if qdq_enabled:
                op_type = pattern[1]
            else:
                op_type = pattern[0]
            if op_type in res:
                res[op_type].append(pattern)
        
        return res

    def generate_internal_patterns(self):
        """Translate the patterns defined in the yaml to internal pattern expression.
        """
        def _generate_pattern(data):
            length = [len(i) for i in data]
            res=[]
            for index in range(max(length)):
                if index <= min(length) - 1:
                    tmp = [i[index] for i in data]
                    if len(set(tmp)) == 1:
                        res.append([tmp[0]])
                    else:
                        res.append(tuple(set(tmp)))
                else:
                    tmp1 = [i[index] for i in data if len(i) > index]
                    res.append(tuple(set(tmp1)))

            return res

        op_level_sequences = {}

        for k, op_level_all_sequences in self.get_eightbit_patterns().items():
            op_level_sequences[k] = []
            sorted_sequences = sorted(op_level_all_sequences)
            last_len = 1
            each_combination = []
            for index, value in enumerate(sorted_sequences):
                if  len(value) >= last_len:
                    last_len = len(value)
                    each_combination.append(value)
                else:
                    op_level_sequences[k].append(copy.deepcopy(each_combination))
                    each_combination.clear()
                    each_combination.append(value)
                    last_len = len(value)

                if index == len(sorted_sequences) - 1:
                    op_level_sequences[k].append(copy.deepcopy(each_combination))

        final_out = []
        for _ , op_level_sequences in op_level_sequences.items():
            for similar_sequences in op_level_sequences:
                final_out.append(_generate_pattern(similar_sequences))

        return final_out
