"""
If the folding passes through a concatenation layer
we need to gather the correct indices to edit.

Note that we need to find the indices only we are before the concatenation layer
"""
from batch_normalization_folding.TensorFlow.graph_path import GraphPath
from typing import Dict, Tuple
import tensorflow as tf


def get_graph_as_dict(model: tf.keras.Model) -> Dict[str, list]:
    """
    This function returns a dictionnary of the layers and their corresponding
    input layers.
    """
    network_dict = {model.layers[0].name: []}
    for layer in model.layers:
        for node in layer._outbound_nodes:
            layer_name = node.outbound_layer.name
            if layer_name not in network_dict:
                network_dict.update({layer_name: [layer.name]})
            else:
                if layer.name not in network_dict[layer_name]:
                    network_dict[layer_name].append(layer.name)
    return network_dict


def reverse_graph(graph: Dict[str, list]) -> Dict[str, list]:
    """
    This function fetches the output layers of each layer of the DNN
    """
    output_dict = {}
    for key_1 in list(graph.keys()):
        for key_2 in graph[key_1]:
            if key_2 not in output_dict:
                output_dict.update({key_2: [key_1]})
            else:
                if key_1 not in output_dict[key_2]:
                    output_dict[key_2].append(key_1)
    for key, values in graph.items():
        for value in values:
            if value not in output_dict:
                output_dict[value] = []
        if key not in output_dict:
            output_dict[key] = []
    return output_dict


def gather_indices_for_concat_layer(
    layer_name: str,
    input_network_dict: Dict[str, list],
    output_network_dict: Dict[str, list],
    model: tf.keras.Model,
) -> Dict[str, Tuple[int, int]]:
    output = {}
    starting_idx = 0
    for name in input_network_dict[layer_name]:
        current_size = model.get_layer(name).output_shape[-1]
        output[name] = (starting_idx, starting_idx + current_size)
        starting_idx += current_size
    return output


def create_dict_from_concatenation_layers(
    model: tf.keras.Model,
) -> Dict[str, Dict[str, Tuple[int, int]]]:
    output = {}
    input_network_dict = get_graph_as_dict(model=model)
    output_network_dict = reverse_graph(graph=input_network_dict)
    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.Concatenate):
            output[layer.name] = gather_indices_for_concat_layer(
                layer_name=layer.name,
                input_network_dict=input_network_dict,
                output_network_dict=output_network_dict,
                model=model,
            )
    return output


def check_for_concatenation_in_path(
    concatenation_indices: Dict[str, Dict[str, Tuple[int, int]]],
    path: list,
    model: tf.keras.Model,
) -> Tuple[bool, list]:
    contains_concat = False
    indices_list = []
    for cpt_e, e in enumerate(path):
        isinstance_concat = isinstance(model.get_layer(e), tf.keras.layers.Concatenate)
        contains_concat = contains_concat or isinstance_concat
        if isinstance_concat:
            previous_in_dict = path[cpt_e - 1] in concatenation_indices[e]
            next_in_dict = path[cpt_e + 1] in concatenation_indices[e]
            if previous_in_dict and next_in_dict:
                indices_list.append((-1, -1))
            elif (not previous_in_dict) and (not next_in_dict):
                indices_list.append((0, model.get_layer(e).output_shape[-1]))
            else:
                if previous_in_dict:
                    b = concatenation_indices[e][path[cpt_e - 1]]
                    indices_list.append(b)
                elif next_in_dict:
                    b = concatenation_indices[e][path[cpt_e + 1]]
                    indices_list.append(b)
                else:
                    indices_list.append((-1, -1))
    return contains_concat, indices_list


def handle_index_list(indices_list: list) -> Tuple[int, int]:
    if (-1, -1) in indices_list or len(indices_list) < 1:
        return (-1, -1)
    a = indices_list[-1][0]
    b = indices_list[-1][1]
    for a_, b_ in indices_list[:-1:-1]:
        a = a_
        b = a_ + b
        if b > b_:
            return (-1, -1)
    return (a, b)


def handle_a_bn(
    concatenation_indices: Dict[str, Dict[str, Tuple[int, int]]],
    model: tf.keras.Model,
    bn_layer_name: str,
    roots: list,
    leaves: list,
    forward: bool,
    graph: GraphPath,
) -> bool:
    contains_concat = False
    for root in roots:
        with_concat, indices_list = check_for_concatenation_in_path(
            concatenation_indices=concatenation_indices,
            path=graph(source=bn_layer_name, destination=root),
            model=model,
        )
        correct_indices = handle_index_list(indices_list=indices_list)
        contains_concat = contains_concat or with_concat
    for leaf in leaves:
        with_concat, indices_list = check_for_concatenation_in_path(
            concatenation_indices=concatenation_indices,
            path=graph(source=bn_layer_name, destination=leaf),
            model=model,
        )
        correct_indices = handle_index_list(indices_list=indices_list)
        contains_concat = contains_concat or with_concat
    return contains_concat


def handle_concatenation_layer(
    model: tf.keras.Model,
    graph_as_dict: Dict[str, list],
    fold_dict: Dict[str, Tuple[list, list, bool]],
) -> Dict[str, Tuple[list, list, bool]]:
    concatenation_indices = create_dict_from_concatenation_layers(model=model)
    graph = GraphPath(graph_as_dict)
    elements_to_remove = []
    for bn_layer_name, (roots, leaves, forward) in fold_dict.items():
        to_remove = handle_a_bn(
            concatenation_indices=concatenation_indices,
            model=model,
            bn_layer_name=bn_layer_name,
            roots=roots,
            leaves=leaves,
            forward=forward,
            graph=graph,
        )
        if to_remove:
            elements_to_remove.append(bn_layer_name)
    for elem_to_remove in elements_to_remove:
        del fold_dict[elem_to_remove]
    return fold_dict
