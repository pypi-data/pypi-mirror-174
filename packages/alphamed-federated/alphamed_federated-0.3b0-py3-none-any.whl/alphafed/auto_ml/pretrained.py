"""An easy way to get pretrained auto models."""

from typing import Tuple

from .auto_model import AutoModel, AutoModelFamily
from .cv import AUTO_MODEL_FAMILIES as CV_AUTO_MODEL_FAMILIES
from .exceptions import ConfigError

_AUTO_MODEL_FAMILIES: Tuple[AutoModelFamily] = (*CV_AUTO_MODEL_FAMILIES, )


def from_pretrained(name: str,
                    meta_data: dict,
                    resource_dir: str,
                    dataset_dir: str,
                    **kwargs) -> AutoModel:
    """Initiate an AutoModel instance from pretrained models.

    Args:
        meta_data:
            The metadata of the pretrained model.
        resource_dir:
            The root dir of the resource for setup process, i.e. parameter files.
        dataset_dir:
            The root dir of the dataset staff.
        kwargs:
            Other keyword arguments.
    """
    if not name:
        raise ConfigError('Must specify the name of auto model.')
    for _family in _AUTO_MODEL_FAMILIES:
        auto_class = _family.get_auto_model(name)
        if auto_class is not None:
            return auto_class(meta_data=meta_data,
                              resource_dir=resource_dir,
                              dataset_dir=dataset_dir,
                              **kwargs)
    raise ConfigError(f'No auto model found for name: {name}.')
