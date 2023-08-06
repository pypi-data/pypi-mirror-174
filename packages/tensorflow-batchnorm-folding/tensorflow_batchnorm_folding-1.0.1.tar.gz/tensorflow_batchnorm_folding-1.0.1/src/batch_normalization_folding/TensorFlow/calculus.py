import numpy as np
from typing import Tuple


def fold_leaf_backward_conv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, W.shape[3]],
    )
    gamma = np.tile(
        np.expand_dims(gamma, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    beta = np.tile(
        np.expand_dims(beta, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    mu = np.tile(
        np.expand_dims(mu, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    sigma = np.tile(
        np.expand_dims(sigma, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    new_b = (
        b
        - np.sum(beta * W, axis=(0, 1, 2))
        + np.sum(W * gamma * (mu / np.sqrt(sigma + 1.0e-3)), axis=(0, 1, 2))
    )
    return (new_W, new_b)


def fold_leaf_backward_dense(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=0), [W.shape[0], 1]
    )
    new_b = (
        b
        - np.sum(beta * W, axis=0)
        + np.sum(W * gamma * (mu / np.sqrt(sigma + 1.0e-3)), axis=0)
    )
    return (new_W, new_b)


def fold_leaf_backward_depthwiseconv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, 1],
    )
    gamma = np.tile(
        np.expand_dims(gamma, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    beta = np.tile(
        np.expand_dims(beta, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    mu = np.tile(
        np.expand_dims(mu, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    sigma = np.tile(
        np.expand_dims(sigma, axis=(0, 1, 3)), [W.shape[0], W.shape[1], 1, W.shape[3]]
    )
    new_b = (
        b
        - np.sum(beta * W, axis=(0, 1, 3))
        + np.sum(W * gamma * (mu / np.sqrt(sigma + 1.0e-3)), axis=(0, 1, 3))
    )
    return (new_W, new_b)


def fold_leaf_backward_bn(
    gamma_: np.ndarray,
    beta_: np.ndarray,
    mu_: np.ndarray,
    sigma_: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """ """
    new_gamma = gamma_ * np.sqrt(sigma + 1.0e-3) / gamma
    new_beta = beta_
    new_mu = beta - mu + gamma * mu_ / (sigma + 1.0e-3)
    new_sigma = sigma_
    return (new_gamma, new_beta, new_mu, new_sigma)


def fold_root_backward_conv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=(0, 1, 2)),
        [W.shape[0], W.shape[1], W.shape[2], 1],
    )
    new_b = (gamma * (b - mu) / np.sqrt(sigma + 1.0e-3)) + beta
    return (new_W, new_b)


def fold_root_backward_dense(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=0), [W.shape[0], 1]
    )
    new_b = (gamma * (b - mu) / np.sqrt(sigma + 1.0e-3)) + beta
    return (new_W, new_b)


def fold_root_backward_depthwiseconv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, W.shape[3]],
    )
    new_b = (gamma * (b - mu) / np.sqrt(sigma + 1.0e-3)) + beta
    return (new_W, new_b)


def fold_root_backward_bn(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = gamma * (W / (sigma + 1.0e-3))
    new_b = gamma * (b - mu) / (sigma + 1.0e-3) + beta
    return (new_W, new_b)


def fold_leaf_forward_conv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=(0, 1, 2)),
        [W.shape[0], W.shape[1], W.shape[2], 1],
    )
    new_b = (gamma * (b + mu) / np.sqrt(sigma + 1.0e-3)) - beta
    return (new_W, new_b)


def fold_leaf_forward_depthwiseconv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, 1],
    )
    new_b = (gamma * (b + mu) / np.sqrt(sigma + 1.0e-3)) - beta
    return (new_W, new_b)


def fold_leaf_forward_dense(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W / np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=0), [W.shape[0], 1]
    )
    new_b = (gamma * (b + mu) / np.sqrt(sigma + 1.0e-3)) - beta
    return (new_W, new_b)


def fold_leaf_forward_bn(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    return (W, b)


def fold_root_forward_conv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, W.shape[3]],
    )
    new_b = (
        b
        + np.sum(
            np.tile(
                np.expand_dims(beta, axis=(0, 1, 3)),
                [W.shape[0], W.shape[1], 1, W.shape[3]],
            )
            * W,
            axis=(0, 1, 2),
        )
        - np.sum(
            W
            * np.tile(
                np.expand_dims(gamma * (mu / np.sqrt(sigma + 1.0e-3)), axis=(0, 1, 3)),
                [W.shape[0], W.shape[1], 1, W.shape[3]],
            ),
            axis=(0, 1, 2),
        )
    )
    return (new_W, new_b)


def fold_root_forward_depthwiseconv(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=(0, 1, 3)),
        [W.shape[0], W.shape[1], 1, 1],
    )
    new_b = (
        b
        + np.sum(beta * W, axis=(0, 1, 3))
        - np.sum(W * gamma * (mu / np.sqrt(sigma + 1.0e-3)), axis=(0, 1, 3))
    )
    return (new_W, new_b)


def fold_root_forward_dense(
    W: np.ndarray,
    b: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """ """
    new_W = W * np.tile(
        np.expand_dims(gamma / np.sqrt(sigma + 1.0e-3), axis=1), [1, W.shape[1]]
    )
    new_b = (
        b
        + np.sum(np.tile(np.expand_dims(beta, axis=1), [1, W.shape[1]]) * W, axis=0)
        - np.sum(
            W
            * np.tile(
                np.expand_dims(gamma * (mu / np.sqrt(sigma + 1.0e-3)), axis=1),
                [1, W.shape[1]],
            ),
            axis=0,
        )
    )
    return (new_W, new_b)


def fold_root_forward_bn(
    gamma_: np.ndarray,
    beta_: np.ndarray,
    mu_: np.ndarray,
    sigma_: np.ndarray,
    gamma: np.ndarray,
    beta: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """ """
    new_gamma = 0
    new_beta = 0
    new_mu = 0
    new_sigma = 0
    return (new_gamma, new_beta, new_mu, new_sigma)
