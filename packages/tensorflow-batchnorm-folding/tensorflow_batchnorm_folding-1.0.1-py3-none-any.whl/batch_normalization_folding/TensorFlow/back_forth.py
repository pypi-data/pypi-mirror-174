from batch_normalization_folding.TensorFlow.to_fold_or_not_to_fold import (
    check_layer_can_be_folded,
)
from typing import Dict, Tuple
import tensorflow as tf


def check_layer(
    model: tf.keras.Model,
    layer: tf.keras.layers.Layer,
    forward_graph: Dict[str, list],
    backward_graph: Dict[str, list],
) -> Tuple[bool, list, list]:
    """
    check if a layer can be folded
    forward and backward
    """
    forward = False
    foldeable, roots, leaves = check_layer_can_be_folded(
        model=model,
        layer=layer,
        forward_graph=backward_graph,
        backward_graph=forward_graph,
        forward=forward,
    )
    if not foldeable:
        forward = True
        foldeable, roots, leaves = check_layer_can_be_folded(
            model=model,
            layer=layer,
            forward_graph=forward_graph,
            backward_graph=backward_graph,
            forward=forward,
        )
    return foldeable, roots, leaves, forward
