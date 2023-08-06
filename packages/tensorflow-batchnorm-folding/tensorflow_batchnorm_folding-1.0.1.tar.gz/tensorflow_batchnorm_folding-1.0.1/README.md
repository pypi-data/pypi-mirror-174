# Batch-Normalization Folding

In this repository, we propose an implementation of the batch-normalization folding algorithm from [IJCAI 2022](https://arxiv.org/pdf/2203.14646.pdf). Batch-Normalization Folding consists in emoving batch-normalization layers without changing the predictive function defiend by the neural network. The simpliest scenario is an application for a fully-connected layer followed by a batch-normalization layer, we get
```math
x \mapsto \gamma \frac{Ax + b - \mu}{\sigma + \epsilon} + \beta = \gamma \frac{A}{\sigma +\epsilon} x + \frac{b - \mu}{\sigma + \epsilon} + \beta
```
Thus the two layers can be expressed as a single fully-connected layer at inference without any change in the predictive function.

## use

This repository is available as a pip package (use `pip install tensorflow-batchnorm-folding`).
This implementation is compatible with tf.keras.Model instances. It was tested with the following models
- [x] ResNet 50
- [x] MobileNet V2
- [x] MobileNet V3
- [x] EfficentNet B0

To run a simple test:
```python
from batch_normalization_folding.folder import fold_batchnormalization_layers
import tensorflow as tf
mod=tf.keras.applications.efficientnet.EfficientNetB0()
folded_model,output_str=fold_batchnormalization_layers(mod,True)
```
The `output_str` is either the ratio num_layers_folded/num_layers_not_folded or 'failed' to state a failure in the process.

## To Do

- [x] unit test on all keras applciations models
- [x] check package installement
- [ ] deal with Concatenate layers

## cite

```
@inproceedings{yvinec2022fold,
  title={To Fold or Not to Fold: a Necessary and Sufficient Condition on Batch-Normalization Layers Folding},
  author={Yvinec, Edouard and Dapogny, Arnaud and Bailly, Kevin},
  journal={IJCAI},
  year={2022}
}
```

## Performance on Base Models

```
+------------------------------------+
|             ResNet 50              |
+------------------------------------+
| BN layers folded         |    53   |
| BN layers not folded     |    0    |
+------------------------------------+
|          EfficientNet B0           |
+------------------------------------+
| BN layers folded         |    49   |
| BN layers not folded     |    0    |
+------------------------------------+
|            MobileNet V2            |
+------------------------------------+
| BN layers folded         |    52   |
| BN layers not folded     |    0    |
+------------------------------------+
|            MobileNet V3            |
+------------------------------------+
| BN layers folded         |    34   |
| BN layers not folded     |    0    |
+------------------------------------+
|        Inception ResNet V2         |
+------------------------------------+
| BN layers folded         |   204   |
| BN layers not folded     |    0    |
+------------------------------------+
|            Inception V3            |
+------------------------------------+
| BN layers folded         |    94   |
| BN layers not folded     |    0    |
+------------------------------------+
|               NASNet               |
+------------------------------------+
| BN layers folded         |    28   |
| BN layers not folded     |   164   |
+------------------------------------+
|            DenseNet 121            |
+------------------------------------+
| BN layers folded         |    59   |
| BN layers not folded     |    62   |
+------------------------------------+
```
