import tensorflow as tf
from typing import Dict, Any


def get_graph_as_dict(model: tf.keras.Model) -> Dict[str, Dict[str, list]]:
    """
    This function returns a dictionnary of the layers and their corresponding
    input layers. This serves the purpose of re-defining the graph with
    new layers.
    """
    network_dict = {"input": {}, "new_output": {}}
    for layer in model.layers:
        for node in layer._outbound_nodes:
            layer_name = node.outbound_layer.name
            if layer_name not in network_dict["input"]:
                network_dict["input"].update({layer_name: [layer.name]})
            else:
                if layer.name not in network_dict["input"][layer_name]:
                    network_dict["input"][layer_name].append(layer.name)
    network_dict["new_output"].update({model.layers[0].name: model.input})
    return network_dict
