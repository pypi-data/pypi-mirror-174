"""Pretraining DenseNet models and schedulers.

Reference: https://arxiv.org/abs/1608.06993
"""

import os
from collections import OrderedDict
from typing import List, Optional, Tuple, Union

import torch
import torch.nn.functional as F
from torch import nn

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

_TensorOrTensorList = Union[torch.Tensor, List[torch.Tensor]]


class _DenseLayer(nn.Module):
    def __init__(self,
                 num_input_features: int,
                 growth_rate: int,
                 bn_size: int,
                 drop_rate: float) -> None:
        super().__init__()
        self.norm1 = nn.BatchNorm2d(num_input_features)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv1 = nn.Conv2d(num_input_features,
                               bn_size * growth_rate,
                               kernel_size=1,
                               stride=1,
                               bias=False)

        self.norm2 = nn.BatchNorm2d(bn_size * growth_rate)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(bn_size * growth_rate,
                               growth_rate,
                               kernel_size=3,
                               stride=1,
                               padding=1,
                               bias=False)

        self.drop_rate = float(drop_rate)

    def forward(self, prev_features: _TensorOrTensorList) -> torch.Tensor:
        if isinstance(input, torch.Tensor):
            prev_features = [prev_features]

        concated_features = torch.cat(prev_features, dim=1)
        bottleneck_output = self.conv1(self.relu1(self.norm1(concated_features)))
        new_features = self.conv2(self.relu2(self.norm2(bottleneck_output)))
        if self.drop_rate > 0:
            new_features = F.dropout(new_features, p=self.drop_rate, training=self.training)
        return new_features


class _DenseBlock(nn.ModuleDict):

    def __init__(self,
                 num_layers: int,
                 num_input_features: int,
                 bn_size: int,
                 growth_rate: int,
                 drop_rate: float) -> None:
        super().__init__()
        for i in range(num_layers):
            layer = _DenseLayer(num_input_features + i * growth_rate,
                                growth_rate=growth_rate,
                                bn_size=bn_size,
                                drop_rate=drop_rate)
            self.add_module(f'denselayer{i + 1}', layer)

    def forward(self, init_features: torch.Tensor) -> torch.Tensor:
        features = [init_features]
        for _layer in self.values():
            new_features = _layer(features)
            features.append(new_features)
        return torch.cat(features, dim=1)


class _Transition(nn.Sequential):
    def __init__(self, num_input_features: int, num_output_features: int) -> None:
        super().__init__()
        self.norm = nn.BatchNorm2d(num_input_features)
        self.relu = nn.ReLU(inplace=True)
        self.conv = nn.Conv2d(num_input_features,
                              num_output_features,
                              kernel_size=1,
                              stride=1,
                              bias=False)
        self.pool = nn.AvgPool2d(kernel_size=2, stride=2)


class DenseNet(nn.Module):
    """Densenet-BC model class.

    Args:
        growth_rate (int):
            How many filters to add each layer (`k` in paper).
        block_config (list of 4 ints):
            How many layers in each pooling block.
        num_init_features (int):
            The number of filters to learn in the first convolution layer.
        bn_size (int):
            Multiplicative factor for number of bottle neck layers.
            (i.e. bn_size * k features in the bottleneck layer)
        drop_rate (float):
            Dropout rate after each dense layer.
        num_classes (int):
            Number of classification classes.
    """

    def __init__(self,
                 growth_rate: int = 32,
                 block_config: Tuple[int, int, int, int] = (6, 12, 24, 16),
                 num_init_features: int = 64,
                 bn_size: int = 4,
                 drop_rate: float = 0,
                 num_classes: int = 1000) -> None:
        super().__init__()

        # First convolution
        self.features = nn.Sequential(
            OrderedDict([
                ('conv0', nn.Conv2d(
                    3, num_init_features, kernel_size=7, stride=2, padding=3, bias=False
                )),
                ('norm0', nn.BatchNorm2d(num_init_features)),
                ('relu0', nn.ReLU(inplace=True)),
                ('pool0', nn.MaxPool2d(kernel_size=3, stride=2, padding=1)),
            ])
        )

        # Each denseblock
        num_features = num_init_features
        for i, num_layers in enumerate(block_config):
            block = _DenseBlock(num_layers=num_layers,
                                num_input_features=num_features,
                                bn_size=bn_size,
                                growth_rate=growth_rate,
                                drop_rate=drop_rate)
            self.features.add_module(f'denseblock{i + 1}', block)

            num_features = num_features + num_layers * growth_rate
            if i != len(block_config) - 1:
                trans = _Transition(num_input_features=num_features,
                                    num_output_features=num_features // 2)
                self.features.add_module(f'transition{i + 1}', trans)
                num_features = num_features // 2

        # Final batch norm
        self.features.add_module('norm5', nn.BatchNorm2d(num_features))

        # Linear layer
        self.classifier = nn.Linear(num_features, num_classes)

        # Official init from torch repo.
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.features(x)
        out = F.relu(features, inplace=True)
        out = F.adaptive_avg_pool2d(out, (1, 1))
        out = torch.flatten(out, 1)
        out = self.classifier(out)
        return out

    def _replace_classifier(self, num_classes: int):
        # replace model's classifier(linear) layer
        num_features = self.classifier.in_features
        self.classifier = nn.Linear(num_features, num_classes)
        nn.init.constant_(self.classifier.bias, 0)


class DenseNet121(DenseNet):

    def __init__(self, num_classes: Optional[int] = 1000) -> None:
        assert (
            num_classes is None or num_classes > 0
        ), 'num_classes must be a positive interger or None.'
        super().__init__(block_config=(6, 12, 24, 16),
                         num_init_features=64,
                         num_classes=num_classes)
        if num_classes is not None:
            self._replace_classifier(num_classes=num_classes)


class DenseNet169(DenseNet):

    def __init__(self, num_classes: Optional[int] = 1000) -> None:
        assert (
            num_classes is None or num_classes > 0
        ), 'num_classes must be a positive interger or None.'
        super().__init__(block_config=(6, 12, 32, 32),
                         num_init_features=64,
                         num_classes=num_classes)
        if num_classes is not None:
            self._replace_classifier(num_classes=num_classes)


class DenseNet201(DenseNet):

    def __init__(self, num_classes: Optional[int] = 1000) -> None:
        assert (
            num_classes is None or num_classes > 0
        ), 'num_classes must be a positive interger or None.'
        super().__init__(block_config=(6, 12, 48, 32),
                         num_init_features=64,
                         num_classes=num_classes)
        if num_classes is not None:
            self._replace_classifier(num_classes=num_classes)


class DenseNet161(DenseNet):

    def __init__(self, num_classes: Optional[int] = 1000) -> None:
        assert (
            num_classes is None or num_classes > 0
        ), 'num_classes must be a positive interger or None.'
        super().__init__(growth_rate=48,
                         block_config=(6, 12, 36, 24),
                         num_init_features=96,
                         num_classes=num_classes)
        if num_classes is not None:
            self._replace_classifier(num_classes=num_classes)
