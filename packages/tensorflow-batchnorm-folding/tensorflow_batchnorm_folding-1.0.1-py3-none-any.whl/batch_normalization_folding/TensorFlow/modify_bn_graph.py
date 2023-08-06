from batch_normalization_folding.TensorFlow.lambda_layers import call_lambda_layer
import tensorflow as tf
from typing import Dict


def remove_folded_layers(
    model: tf.keras.Model, backward_graph: Dict[str, list], fold_dict: Dict[str, tuple]
) -> tf.keras.Model:
    """
    This function edits a neural network graph by removing the target layers
    Here the layers will systematically be batch-normalization layers
    """
    network_dict = {}
    network_dict["input_layers_of"] = backward_graph
    network_dict["new_output_tensor_of"] = {model.layers[0].name: model.input}
    model_outputs = []
    intermediate_outputs = {model.layers[0].name: model.input}
    for cpt, layer in enumerate(model.layers[1:]):
        layer_input = [
            network_dict["new_output_tensor_of"][layer_aux]
            for layer_aux in network_dict["input_layers_of"][layer.name]
        ]
        if len(layer_input) == 1:
            layer_input = layer_input[0]
        if layer.name in fold_dict:
            x = intermediate_outputs[network_dict["input_layers_of"][layer.name][0]]
            intermediate_outputs[layer.name] = x
        else:
            if len(network_dict["input_layers_of"][layer.name]) == 1 or isinstance(
                layer, tf.keras.layers.Lambda
            ):
                x = call_lambda_layer(
                    layer_input=layer_input, model=model, layer=layer, layer_cpt=cpt + 1
                )
                intermediate_outputs[layer.name] = x
            else:
                if (
                    isinstance(layer, tf.keras.layers.Add)
                    or isinstance(layer, tf.keras.layers.Multiply)
                    or isinstance(layer, tf.keras.layers.Concatenate)
                ):
                    x = layer(
                        [
                            intermediate_outputs[elem]
                            for elem in network_dict["input_layers_of"][layer.name]
                        ]
                    )
                else:
                    x = layer(
                        intermediate_outputs[
                            network_dict["input_layers_of"][layer.name][0]
                        ],
                        intermediate_outputs[
                            network_dict["input_layers_of"][layer.name][1]
                        ],
                    )
                intermediate_outputs[layer.name] = x
        network_dict["new_output_tensor_of"].update({layer.name: x})
        if layer.name in model.output_names:
            model_outputs.append(x)
    output_model = tf.keras.Model(inputs=model.inputs, outputs=model_outputs[-1])
    for layer in output_model.layers:
        for node in layer._outbound_nodes:
            layer_name = node.outbound_layer.name
            if layer_name in fold_dict:
                layer._outbound_nodes.remove(node)
                if "_outbound_nodes_value" in dir(layer):
                    if node in layer._outbound_nodes_value:
                        layer._outbound_nodes_value.remove(node)
    output_model._name = model.name
    return output_model
