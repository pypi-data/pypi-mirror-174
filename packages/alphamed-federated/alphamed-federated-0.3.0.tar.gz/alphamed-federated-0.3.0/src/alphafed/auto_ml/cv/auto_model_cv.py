"""Define base AutoModel interfaces in CV tasks."""


from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Tuple

import torch

from ..auto_model import Meta


@dataclass
class AutoMetaImageInput(Meta):

    image_size: Tuple[int, int]

    @classmethod
    def from_json(cls, data: dict) -> 'AutoMetaImageInput':
        assert data and isinstance(data, dict), f'Invalid image meta data: {data}'
        image_size = data.get('image_size')
        assert (
            image_size and isinstance(image_size, list) and len(image_size) == 2
        ), f'Invalid image meta data: {data}'
        return AutoMetaImageInput(image_size=tuple(image_size))


class Preprocessor(ABC):

    @abstractmethod
    def transform(self, image_file: str) -> torch.Tensor:
        """Transform an image object into an input tensor."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.transform(*args, **kwargs)
