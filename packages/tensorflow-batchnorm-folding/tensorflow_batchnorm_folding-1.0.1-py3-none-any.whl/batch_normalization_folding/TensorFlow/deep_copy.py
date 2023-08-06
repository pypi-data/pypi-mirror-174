import tensorflow as tf


def deep_copy_a_model(model: tf.keras.Model) -> tf.keras.Model:
    """
    performs a deep copy.
    This is important, as we edit the graph and want to make sure
    that we don't edit the base model
    """
    clone = tf.keras.models.clone_model(model)
    first_layer_config = model.get_config()["layers"][0]
    clone.build(first_layer_config["config"]["batch_input_shape"][1:])
    clone.set_weights(model.get_weights())
    clone._name = model.name
    return clone
