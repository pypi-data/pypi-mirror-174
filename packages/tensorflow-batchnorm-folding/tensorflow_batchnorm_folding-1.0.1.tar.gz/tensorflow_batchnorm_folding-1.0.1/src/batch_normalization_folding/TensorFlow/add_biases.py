import sys
from batch_normalization_folding.TensorFlow.lambda_layers import call_lambda_layer
from batch_normalization_folding.TensorFlow.graph_modif import get_graph_as_dict
import tensorflow as tf
from typing import Dict
import numpy as np


def add_conv_bias(layer: tf.keras.layers.Layer) -> tf.keras.layers.Layer:
    """
    This function creates a convolutional layer with a bias
    """
    conf = layer.get_config()
    return tf.keras.layers.Conv2D(
        name=layer.name,
        filters=layer.weights[0].numpy().shape[-1],
        kernel_size=layer.weights[0].numpy().shape[:2],
        strides=conf["strides"],
        padding=conf["padding"],
        activation=conf["activation"],
        use_bias=True,
        kernel_initializer=tf.constant_initializer(value=layer.weights[0].numpy()),
        bias_initializer=tf.constant_initializer(
            value=np.zeros(shape=(layer.weights[0].numpy().shape[-1],))
        ),
    )


def add_depth_bias(layer: tf.keras.layers.Layer) -> tf.keras.layers.Layer:
    """
    This function creates a depthwise layer with a bias
    """
    conf = layer.get_config()
    return tf.keras.layers.DepthwiseConv2D(
        name=layer.name,
        kernel_size=layer.weights[0].numpy().shape[0],
        strides=conf["strides"],
        padding=conf["padding"],
        depth_multiplier=conf["depth_multiplier"],
        activation=conf["activation"],
        groups=conf["groups"],
        dilation_rate=conf["dilation_rate"],
        data_format=conf["data_format"],
        use_bias=True,
        depthwise_initializer=tf.constant_initializer(value=layer.weights[0].numpy()),
        bias_initializer=tf.constant_initializer(
            value=np.zeros(shape=(layer.weights[0].numpy().shape[-2],))
        ),
    )


def add_dense_bias(layer: tf.keras.layers.Layer) -> tf.keras.layers.Layer:
    """
    This function creates a fully-connected/dense layer with a bias
    """
    conf = layer.get_config()
    return tf.keras.layers.Dense(
        name=layer.name,
        units=layer.weights[0].numpy().shape[-1],
        activation=conf["activation"],
        use_bias=True,
        kernel_initializer=tf.constant_initializer(value=layer.weights[0].numpy()),
        bias_initializer=tf.constant_initializer(
            value=np.zeros(shape=(layer.weights[0].numpy().shape[-1],))
        ),
    )


def complete_model(model: tf.keras.Model, layers_to_complete: list) -> tf.keras.Model:
    """
    Batch-Normalization folding requires the expressive layers to use biases
    This function adds those biases to all the expressive layers
    """
    network_dict = get_graph_as_dict(model=model)
    model_outputs = []
    changed_layers = []
    for cpt, layer in enumerate(model.layers[1:]):
        layer_input = [
            network_dict["new_output"][layer_aux]
            for layer_aux in network_dict["input"][layer.name]
        ]
        if len(layer_input) == 1:
            layer_input = layer_input[0]
        if isinstance(layer, tf.keras.layers.Dense):
            if layer.get_config()["use_bias"] or layer.name not in layers_to_complete:
                new_layer = layer
            else:
                new_layer = add_dense_bias(layer=layer)
                changed_layers.append(layer.name)
            x = new_layer(layer_input)
            network_dict["new_output"][layer.name] = x
        elif isinstance(layer, tf.keras.layers.DepthwiseConv2D):
            if layer.get_config()["use_bias"] or layer.name not in layers_to_complete:
                new_layer = layer
            else:
                new_layer = add_depth_bias(layer=layer)
                changed_layers.append(layer.name)
            x = new_layer(layer_input)
            network_dict["new_output"][layer.name] = x
        elif isinstance(layer, tf.keras.layers.Conv2D):
            if layer.get_config()["use_bias"] or layer.name not in layers_to_complete:
                new_layer = layer
            else:
                new_layer = add_conv_bias(layer=layer)
                changed_layers.append(layer.name)
            x = new_layer(layer_input)
            network_dict["new_output"][layer.name] = x
        else:
            if len(network_dict["input"][layer.name]) == 1 or isinstance(
                layer, tf.keras.layers.Lambda
            ):
                x = call_lambda_layer(
                    layer_input=layer_input, model=model, layer=layer, layer_cpt=cpt + 1
                )
                network_dict["new_output"][layer.name] = x
            else:
                if (
                    isinstance(layer, tf.keras.layers.Add)
                    or isinstance(layer, tf.keras.layers.Multiply)
                    or isinstance(layer, tf.keras.layers.Concatenate)
                ):
                    x = layer(
                        [
                            network_dict["new_output"][elem]
                            for elem in network_dict["input"][layer.name]
                        ]
                    )
                else:
                    if "lambda" in str(type(layer)).lower():
                        print(f"Layer {layer.name} can't be", end="")
                        print(f" called because of type {type(layer)}")
                    if len(network_dict["input"][layer.name]) == 2:
                        x = layer(
                            network_dict["new_output"][
                                network_dict["input"][layer.name][0]
                            ],
                            network_dict["new_output"][
                                network_dict["input"][layer.name][1]
                            ],
                        )
                    elif len(network_dict["input"][layer.name]) == 3:
                        x = layer(
                            network_dict["new_output"][
                                network_dict["input"][layer.name][0]
                            ],
                            network_dict["new_output"][
                                network_dict["input"][layer.name][1]
                            ],
                            network_dict["new_output"][
                                network_dict["input"][layer.name][2]
                            ],
                        )
                network_dict["new_output"][layer.name] = x
        if layer.name in model.output_names:
            model_outputs.append(x)
    new_model = tf.keras.Model(inputs=model.inputs, outputs=model_outputs[-1])
    new_model._name = model.name
    return new_model


def check_if_need_completion(
    model: tf.keras.Model, fold_dict: Dict[str, tuple]
) -> list:
    """
    check layer that need a bias modification
    """
    output = []
    for key, (roots, leaves, forward) in fold_dict.items():
        for root in roots:
            l = model.get_layer(root)
            if not isinstance(l, tf.keras.layers.BatchNormalization):
                if not l.get_config()["use_bias"]:
                    output.append(root)
            else:
                print(l.get_config())
        for leaf in leaves:
            l = model.get_layer(leaf)
            if not isinstance(l, tf.keras.layers.BatchNormalization):
                if not l.get_config()["use_bias"]:
                    output.append(leaf)
            else:
                print(l.get_config())
    return output
