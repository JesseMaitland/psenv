from abc import ABC, abstractmethod
from typing import List
from pathlib import Path


class Paths(ABC):

    @property
    @abstractmethod
    def directories(self) -> List[Path]:
        pass

    @property
    @abstractmethod
    def files(self) -> List[Path]:
        pass
