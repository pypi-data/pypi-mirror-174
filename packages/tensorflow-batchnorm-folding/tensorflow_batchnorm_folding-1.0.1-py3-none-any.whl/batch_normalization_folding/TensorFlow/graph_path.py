"""
Gvien a model defiend as a graph in a dict
we get a class that can return the path between
two nodes as a list of strings (names of the layers)
"""
from sknetwork.path import get_shortest_path

import numpy as np
from typing import Any, Dict


class GraphPath:
    def __init__(self, graph_as_dict: Dict[str, list]) -> None:
        self.graph_as_dict = graph_as_dict
        self.convert_dict_to_matrix()

    def convert_dict_to_matrix(self):
        self.l = len(self.graph_as_dict)
        self.adjacency_matrix = np.zeros(shape=(self.l, self.l))
        self.name_to_id = {key: cpt for cpt, key in enumerate(self.graph_as_dict)}
        self.id_to_name = {cpt: key for cpt, key in enumerate(self.graph_as_dict)}
        for key, values in self.graph_as_dict.items():
            for key_ in values:
                self.adjacency_matrix[self.name_to_id[key], self.name_to_id[key_]] = 1
                self.adjacency_matrix[self.name_to_id[key_], self.name_to_id[key]] = 1

    def search_path_between_two_nodes(self, source: str, destination: str) -> list:
        return get_shortest_path(
            adjacency=self.adjacency_matrix,
            sources=self.name_to_id[source],
            targets=self.name_to_id[destination],
        )

    def __call__(self, source: str, destination: str, *args: Any, **kwds: Any) -> list:
        path = self.search_path_between_two_nodes(
            source=source, destination=destination
        )
        path_str = [self.id_to_name[e] for e in path]
        return path_str


if __name__ == "__main__":
    import tensorflow as tf

    model = tf.keras.applications.resnet50.ResNet50(weights=None)

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

    print("ResNet 50")
    model_dict = get_graph_as_dict(model=model)
    model_graph = GraphPath(graph_as_dict=model_dict)

    print(
        f"searching path from node {model.layers[4].name} to node {model.layers[28].name}"
    )
    path = model_graph(source=model.layers[4].name, destination=model.layers[28].name)
    for e in path:
        print(f"\t{e}")

    model = tf.keras.applications.densenet.DenseNet121(weights=None)
    print("DenseNet 121")
    model_dict = get_graph_as_dict(model=model)
    model_graph = GraphPath(graph_as_dict=model_dict)

    print(
        f"searching path from node {model.layers[24].name} to node {model.layers[34].name}"
    )
    path = model_graph(source=model.layers[24].name, destination=model.layers[34].name)
    for e in path:
        print(f"\t{e}")
