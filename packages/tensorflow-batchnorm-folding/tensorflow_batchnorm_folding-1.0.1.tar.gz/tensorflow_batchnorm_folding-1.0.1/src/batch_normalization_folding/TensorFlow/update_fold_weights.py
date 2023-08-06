from batch_normalization_folding.TensorFlow.calculus import *
import tensorflow as tf
import numpy as np
from typing import Dict
import sys


def fold_leaf_forward(
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    layer: tf.keras.layers.Layer,
):
    """ """
    if isinstance(layer, tf.keras.layers.Conv2D):
        layer.set_weights(
            fold_leaf_forward_conv(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    elif isinstance(layer, tf.keras.layers.DepthwiseConv2D):
        layer.set_weights(
            fold_leaf_forward_depthwiseconv(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    elif isinstance(layer, tf.keras.layers.Dense):
        layer.set_weights(
            fold_leaf_forward_dense(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    else:
        print(f"folding foward leaf of type BN is not supported yet")
        sys.exit()


def fold_leaf_backward(
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    layer: tf.keras.layers.Layer,
):
    """ """
    if isinstance(layer, tf.keras.layers.Conv2D):
        layer.set_weights(
            fold_leaf_backward_conv(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    elif isinstance(layer, tf.keras.layers.DepthwiseConv2D):
        layer.set_weights(
            fold_leaf_backward_depthwiseconv(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    elif isinstance(layer, tf.keras.layers.Dense):
        layer.set_weights(
            fold_leaf_backward_dense(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    else:
        layer.set_weights(
            fold_leaf_backward_bn(
                gamma_=layer.weights[0].numpy(),
                beta_=layer.weights[1].numpy(),
                mu_=layer.weights[2].numpy(),
                sigma_=layer.weights[3].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )


def fold_leaf(
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    layer: tf.keras.layers.Layer,
    forward: bool,
):
    """ """
    if forward:
        fold_leaf_forward(gamma=gamma, beta=beta, mu=mu, sigma=sigma, layer=layer)
    else:
        fold_leaf_backward(gamma=gamma, beta=beta, mu=mu, sigma=sigma, layer=layer)


def fold_root_forward(
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    layer: tf.keras.layers.Layer,
):
    """ """
    if isinstance(layer, tf.keras.layers.Conv2D):
        layer.set_weights(
            fold_root_forward_conv(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    elif isinstance(layer, tf.keras.layers.DepthwiseConv2D):
        layer.set_weights(
            fold_root_forward_depthwiseconv(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    elif isinstance(layer, tf.keras.layers.Dense):
        layer.set_weights(
            fold_root_forward_dense(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    else:
        print(f"folding foward root of type BN is not supported yet")
        sys.exit()


def fold_root_backward(
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    layer: tf.keras.layers.Layer,
):
    """ """
    if isinstance(layer, tf.keras.layers.Conv2D):
        layer.set_weights(
            fold_root_backward_conv(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    elif isinstance(layer, tf.keras.layers.DepthwiseConv2D):
        layer.set_weights(
            fold_root_backward_depthwiseconv(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    elif isinstance(layer, tf.keras.layers.Dense):
        layer.set_weights(
            fold_root_backward_dense(
                W=layer.weights[0].numpy(),
                b=layer.weights[1].numpy(),
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
            )
        )
    else:
        new_W, new_b = fold_root_backward_bn(
            W=layer.weights[0].numpy(),
            b=layer.weights[1].numpy(),
            gamma=gamma,
            beta=beta,
            mu=mu,
            sigma=sigma,
        )
        layer.set_weights(
            [new_W, new_b, layer.weights[2].numpy(), layer.weights[3].numpy()]
        )


def fold_root(
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
    layer: tf.keras.layers.Layer,
    forward: bool,
):
    """ """
    if forward:
        fold_root_forward(gamma=gamma, beta=beta, mu=mu, sigma=sigma, layer=layer)
    else:
        fold_root_backward(gamma=gamma, beta=beta, mu=mu, sigma=sigma, layer=layer)


def fold_weights(model: tf.keras.Model, fold_dict: Dict[str, tuple]):
    """
    performs the update of the weights to fold
    """
    for layer_name, (roots, leaves, forward) in fold_dict.items():
        bn_weights = model.get_layer(layer_name).weights
        weight_shape = bn_weights[0].numpy().shape
        gamma = np.ones(weight_shape)
        beta = np.zeros(weight_shape)
        mu = np.zeros(weight_shape)
        sigma = np.ones(weight_shape)
        for theta in bn_weights:
            if "gamma:0" in theta.name:
                gamma = theta.numpy()
            elif "beta:0" in theta.name:
                beta = theta.numpy()
            elif "moving_mean:0" in theta.name:
                mu = theta.numpy()
            elif "moving_variance:0" in theta.name:
                sigma = theta.numpy()

        for leaf in leaves:
            fold_leaf(
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
                layer=model.get_layer(leaf),
                forward=forward,
            )
        for root in roots:
            fold_root(
                gamma=gamma,
                beta=beta,
                mu=mu,
                sigma=sigma,
                layer=model.get_layer(root),
                forward=forward,
            )
