import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batch_normalization_folding.TensorFlow.package as check

check.check_packages()
from batch_normalization_folding.TensorFlow.tf_bn_fold import fold_tensorflow_model
import tensorflow as tf
from typing import Any, Tuple
import sys


def fold_batchnormalization_layers(model: Any, verbose: bool) -> Tuple[Any, str]:
    """
    Performs the update of the model for batch norm folding
    """
    if isinstance(model, tf.keras.Model) and not isinstance(model, tf.keras.Sequential):
        return fold_tensorflow_model(model=model, verbose=verbose)
    else:
        print(
            f"\rRequested model type is not supported yet." f" Type is {type(model)}."
        )
        return model, "failed"


if __name__ == "__main__":
    # mod = tf.keras.applications.resnet50.ResNet50(weights=None)
    # mod._name = "ResNet_50"
    # folded_model, output_str = fold_batchnormalization_layers(mod, True)
    # mod = tf.keras.applications.efficientnet.EfficientNetB0(weights=None)
    # mod._name = "EfficientNet_B0"
    # folded_model, output_str = fold_batchnormalization_layers(mod, True)
    # mod = tf.keras.applications.mobilenet_v2.MobileNetV2(weights=None)
    # mod._name = "MobileNet_V2"
    # folded_model, output_str = fold_batchnormalization_layers(mod, True)
    # mod = tf.keras.applications.MobileNetV3Small(weights=None)
    # mod._name = "MobileNet_V3"
    # folded_model, output_str = fold_batchnormalization_layers(mod, True)
    # mod = tf.keras.applications.inception_resnet_v2.InceptionResNetV2(weights=None)
    # mod._name = "Inception_ResNet_V2"
    # folded_model, output_str = fold_batchnormalization_layers(mod, True)
    # mod = tf.keras.applications.inception_v3.InceptionV3(weights=None)
    # mod._name = "Inception_V3"
    # folded_model, output_str = fold_batchnormalization_layers(mod, True)
    # mod = tf.keras.applications.nasnet.NASNetMobile(weights=None)
    # mod._name = "NASNet"
    # folded_model, output_str = fold_batchnormalization_layers(mod, True)
    # mod = tf.keras.applications.densenet.DenseNet121(weights=None)
    # mod._name = "DenseNet_121"
    # folded_model, output_str = fold_batchnormalization_layers(mod, True)
    # print("+--------------------------------+")
    # print(f"|            Summary             |")
    # print("+--------------------------------+")
    # print("|      ResNet 50      |    \033[92m\u2714\033[0m     |")
    # print("|   EfficientNet B0   |    \033[92m\u2714\033[0m     |")
    # print("|    MobileNet V2     |    \033[92m\u2714\033[0m     |")
    # print("|    MobileNet V3     |    \033[92m\u2714\033[0m     |")
    # print("| Inception ResNet V2 |    \033[92m\u2714\033[0m     |")
    # print("|    Inception V3     |    \033[92m\u2714\033[0m     |")
    # print("|    NASNet Mobile    |    \033[92m\u2714\033[0m     |")
    # print("|    DenseNet 121     |    \033[92m\u2714\033[0m     |")
    # print("+--------------------------------+")
    mod = tf.keras.models.load_model("../../../Downloads/keras_decoded.h5")
    mod._name = "GabNet"
    folded_model, output_str = fold_batchnormalization_layers(mod, True)
    import shutil

    def remove_chache_folders(current_repo: str = ""):
        if current_repo == "":
            new_refs = [elem for elem in os.listdir()]
        else:
            new_refs = [current_repo + "/" + elem for elem in os.listdir(current_repo)]
        for elem in new_refs:
            if os.path.isdir(elem):
                if "__pycache__" in elem:
                    shutil.rmtree(elem)
                else:
                    remove_chache_folders(current_repo=elem)

    remove_chache_folders()
