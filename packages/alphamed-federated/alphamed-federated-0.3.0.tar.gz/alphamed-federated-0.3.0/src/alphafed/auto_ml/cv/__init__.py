"""CV pretrained model zoo."""

from .dense_net import DenseNetFamily
from .res_net import ResNetFamily

AUTO_MODEL_FAMILIES = (DenseNetFamily, ResNetFamily)
