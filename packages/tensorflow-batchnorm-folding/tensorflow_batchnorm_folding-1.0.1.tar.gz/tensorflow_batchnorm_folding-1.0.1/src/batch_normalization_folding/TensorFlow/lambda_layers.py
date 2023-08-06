import tensorflow as tf


def get_lambda_args(cpt: int, model: tf.keras.Model, layer_name: str):
    extra_args = model.get_config()["layers"][cpt]["inbound_nodes"][0][-1]
    if "tf.compat.v1.gather" in layer_name:
        return extra_args
    if isinstance(extra_args, list):
        return [-5, 5]  # shitty fix for shitty bug
    if "y" in extra_args:
        return {"y": extra_args["y"]}
    elif "clip_value_min" in extra_args:
        return {
            "clip_value_min": extra_args["clip_value_min"],
            "clip_value_max": extra_args["clip_value_max"],
        }
    else:
        return [value for _, value in extra_args.items()]


def retrieve_layer_cpt(model: tf.keras.Model, layer_name: str) -> int:
    """ """
    for cpt, layer in enumerate(model.layers):
        if layer.name == layer_name:
            return cpt


def call_lambda_layer(
    layer_input: tf.Variable,
    model: tf.keras.Model,
    layer: tf.keras.layers.Layer,
    layer_cpt: int,
) -> tf.Variable:
    """
    this function deals with lambda layers
    the issue is : lambda layers often use parameters
    that are neither weights nor variable and are
    only accessible in the mdoel config
    """
    if not isinstance(layer, tf.keras.layers.Lambda) and not (
        "lambda" in type(layer).__name__.lower()
    ):
        output = layer(layer_input)
        return output
    if layer_cpt == -1:
        layer_cpt = retrieve_layer_cpt(model=model, layer_name=layer.name)
    extra_args = get_lambda_args(cpt=layer_cpt, model=model, layer_name=layer.name)
    if "y" in extra_args:
        output = layer(layer_input, extra_args["y"])
    elif "clip_value_min" in extra_args:
        output = layer(
            layer_input, extra_args["clip_value_min"], extra_args["clip_value_max"]
        )
    elif "tf.compat.v1.gather" in layer.name:
        import sys

        sys.exit()
        output = tf.gather(layer_input, *extra_args[-1])
    else:
        output = layer(layer_input, *extra_args)
    return output
