import glob
import json
import ntpath
import tarfile
import tempfile
from importlib.util import find_spec
from pathlib import Path
from typing import Callable, Optional, Dict, Tuple, Type

import tensorflow as tf  # type: ignore
from keras import Model  # type: ignore
from keras_data_format_converter import convert_channels_first_to_last  # type: ignore
from leap_model_rebuilder import rebuild_model  # type: ignore
from onnx2kerastl import onnx_to_keras  # type: ignore
from onnx2kerastl.exceptions import OnnxUnsupported  # type: ignore
from tensorflow.keras.models import load_model  # type: ignore

from leap_model_parser.contract.importmodelresponse import DatasetInfo, NodeResponse, ImportModelTypeEnum
from leap_model_parser.keras_json_model_import import KerasJsonModelImport

onnx_imported = False
package_name = 'onnx'
spec = find_spec(package_name)
if spec is not None:
    import onnx  # type: ignore

    onnx_imported = True


class ModelParser:
    def __init__(self, should_transform_inputs_and_outputs=False,
                 custom_layers: Optional[Dict[str, Type[tf.keras.layers.Layer]]] = None, dataset_info: Optional[DatasetInfo] = None):
        self._should_transform_inputs_and_outputs = should_transform_inputs_and_outputs
        self.dataset_info = dataset_info
        self.custom_layers = custom_layers
        if custom_layers is None:
            self.custom_layers = {}

        self._model_types_converter = {
            ImportModelTypeEnum.JSON_TF2.value: self.convert_json_model,
            ImportModelTypeEnum.H5_TF2.value: self.convert_h5_model,
            ImportModelTypeEnum.ONNX.value: self.convert_onnx_model,
            ImportModelTypeEnum.PB_TF2.value: self.convert_pb_model,
        }

    def get_keras_model_and_model_graph(
            self, model_path: Path, model_type: ImportModelTypeEnum) -> Tuple[Dict[str, NodeResponse], Optional[Model]]:
        model_to_keras_converter: Optional[Callable[[str], Tuple[Dict[str, NodeResponse], Optional[Model]]]] = \
            self._model_types_converter.get(model_type.value)
        if model_to_keras_converter is None:
            raise Exception(f"Unable to import external version, {str(model_path)} file format isn't supported")

        file_path = str(model_path)
        try:
            model_schema, keras_model = model_to_keras_converter(file_path)
            model_generator = KerasJsonModelImport(self.custom_layers, self.dataset_info)
            graph = model_generator.generate_graph(model_schema)
            return graph, keras_model
        except Exception as e:
            if model_type.value in [ImportModelTypeEnum.H5_TF2.value, ImportModelTypeEnum.PB_TF2.value]:
                if model_type.value == ImportModelTypeEnum.H5_TF2.value:
                    keras_model = self._load_keras_model_with_custom_layers(file_path)
                else:
                    keras_model = self._get_k_model_from_pb_path(file_path)

                rebuilt_model = rebuild_model(keras_model)
                model_schema, keras_model = self.convert_to_keras_model(rebuilt_model)
                model_generator = KerasJsonModelImport(self.custom_layers, self.dataset_info)
                graph = model_generator.generate_graph(model_schema)
                return graph, keras_model
            else:
                raise e

    def _get_k_model_from_pb_path(self, file_path: str):
        tar_file = tarfile.open(file_path)
        with tempfile.TemporaryDirectory() as temp_dir:
            tar_file.extractall(temp_dir)
            pb_files = glob.glob(temp_dir + "/**/*.pb", recursive=True)
            if len(pb_files) == 0:
                raise Exception('no pb files were found')

            pb_file_path = next(iter(pb_files))
            pb_folder_path = next(iter(ntpath.split(pb_file_path)))

            k_model = self._load_keras_model_with_custom_layers(pb_folder_path)
        return k_model

    def generate_model_graph(self, model_path: Path, model_type: ImportModelTypeEnum) -> Dict[str, NodeResponse]:
        model_graph, _ = self.get_keras_model_and_model_graph(model_path, model_type)
        return model_graph

    @classmethod
    def convert_json_model(cls, file_path: str) -> Tuple[Dict[str, NodeResponse], None]:
        with open(file_path, 'r') as f:
            model_schema = json.load(f)
        return model_schema, None

    def convert_pb_model(self, file_path: str) -> Tuple[Dict[str, NodeResponse], Model]:
        k_model = self._get_k_model_from_pb_path(file_path)
        return self.convert_to_keras_model(k_model)

    def convert_onnx_model(self, file_path: str) -> Tuple[Dict[str, NodeResponse], Model]:
        if not onnx_imported:
            raise OnnxUnsupported()

        onnx_model = onnx.load_model(file_path)
        input_all = [_input.name for _input in onnx_model.graph.input]
        input_initializer = [node.name for node in onnx_model.graph.initializer]
        input_names = list(set(input_all) - set(input_initializer))
        k_model = onnx_to_keras(onnx_model, input_names=input_names,
                                name_policy='attach_weights_name')
        return self.convert_to_keras_model(k_model)

    def _load_keras_model_with_custom_layers(self, file_path: str):
        custom_objects = {}
        if self.custom_layers is not None:
            custom_objects = self.custom_layers
        return load_model(file_path, custom_objects=custom_objects, compile=False)

    def convert_h5_model(self, file_path: str) -> Tuple[Dict[str, NodeResponse], Model]:
        imported_model = self._load_keras_model_with_custom_layers(file_path)
        return self.convert_to_keras_model(imported_model)

    def convert_to_keras_model(self, k_model) -> Tuple[Dict[str, NodeResponse], Model]:
        converted_k_model = convert_channels_first_to_last(
            k_model, self._should_transform_inputs_and_outputs, self.custom_layers)

        model_schema = json.loads(converted_k_model.to_json())
        model_schema = replace_dots_in_model_schema(model_schema)

        return model_schema, converted_k_model


def replace_dots_for_tf_ops_inbound_nodes(layer, dot_input_names):
    inbound_nodes_to_enumerate = KerasJsonModelImport.prepare_inbound_nodes(layer['inbound_nodes'][0])
    if len(inbound_nodes_to_enumerate) == 1:
        if layer['inbound_nodes'][0][0] in dot_input_names:
            layer['inbound_nodes'][0][0] = layer['inbound_nodes'][0][0].replace(".", "_")
    elif len(inbound_nodes_to_enumerate) == 2:
        if layer['inbound_nodes'][0][0] in dot_input_names:
            layer['inbound_nodes'][0][0] = layer['inbound_nodes'][0][0].replace(".", "_")
        try:
            if layer['inbound_nodes'][0][-1]['y'][0] in dot_input_names:
                layer['inbound_nodes'][0][0] = layer['inbound_nodes'][0][0].replace(".", "_")
        except KeyError:
            if layer['inbound_nodes'][0][-1]['b'][0] in dot_input_names:
                layer['inbound_nodes'][0][0] = layer['inbound_nodes'][0][0].replace(".", "_")
    else:
        raise Exception('unsupported inbound_nodes')


def replace_dots_in_model_schema(model_schema: dict) -> dict:
    dot_input_names = set()
    for inp_layer in model_schema["config"]["input_layers"]:
        if "." in inp_layer[0]:
            dot_input_names.add(inp_layer[0])
            inp_layer[0] = inp_layer[0].replace(".", "_")
    for layer in model_schema["config"]["layers"]:
        if layer["name"] in dot_input_names:
            layer["name"] = layer["name"].replace(".", "_")
            layer["config"]["name"] = layer["config"]["name"].replace(".", "_")

        if layer["inbound_nodes"] and not isinstance(layer["inbound_nodes"][0][0], list):
            replace_dots_for_tf_ops_inbound_nodes(layer, dot_input_names)
            continue
        for inbound_nodes in layer["inbound_nodes"]:
            for inbound_node in inbound_nodes:
                if inbound_node[0] in dot_input_names:
                    inbound_node[0] = inbound_node[0].replace(".", "_")

    return model_schema
