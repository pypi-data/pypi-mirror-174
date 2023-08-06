"""Define base AutoModel interfaces."""

import os
from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Optional, Type

from .. import logger, task_logger


@unique
class TaskMode(int, Enum):

    LOCAL = 1
    FED_AVG = 2
    HETERO_NN_HOST = 3
    HETERO_NN_COLLABORATOR = 4


@unique
class DatasetMode(int, Enum):

    TRAINING = 1
    VALIDATION = 2
    TESTING = 3


@dataclass
class Meta(ABC):
    ...


@dataclass
class AutoMeta(Meta, metaclass=ABCMeta):
    """Manage meta data of a auto model."""

    name: str


class AutoModel(ABC):
    """An model which supports alphamed AutoML process."""

    def __init__(self,
                 meta_data: dict,
                 resource_dir: str,
                 dataset_dir: str,
                 **kwargs) -> None:
        super().__init__()
        self.meta_data = meta_data
        self.resource_dir = resource_dir
        self.dataset_dir = dataset_dir
        self.annotation_file = os.path.join(dataset_dir, 'annotation.json')

    @abstractmethod
    def train(self):
        """Go into `train` mode as of torch.nn.Module."""

    @abstractmethod
    def eval(self):
        """Go into `eval` mode as of torch.nn.Module."""

    @abstractmethod
    def forward(self, *args, **kwargs):
        """Do a forward propagation as of torch.nn.Module."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.forward(*args, **kwargs)

    @abstractmethod
    def init_dataset(self) -> bool:
        """Init local dataset and report the result."""

    @abstractmethod
    def fine_tune(self, id: str, task_id: str, is_initiator: bool = False, **kwargs):
        """Begin to fine-tune on dataset.

        Args:
            id:
                The ID of current node.
            task_id:
                The ID of current task.
            is_initiator:
                Is current node the initiator of the task.
            kwargs:
                Other keywords for specific models.
        """

    def push_log(self, message: str):
        """Push a running log message to the task manager."""
        assert message and isinstance(message, str), f'invalid log message: {message}'
        if hasattr(self, 'task_id') and self.task_id:
            task_logger.info(message, extra={"task_id": self.task_id})
        else:
            logger.warn('Failed to push a message because context is not initialized.')


class AutoModelFamily(ABC):
    """A serious auto models with the same core architecture."""

    @classmethod
    @abstractmethod
    def get_auto_model(cls, name: str) -> Optional[Type[AutoModel]]:
        """Get the auto model class corresponding to the given name if exists."""
