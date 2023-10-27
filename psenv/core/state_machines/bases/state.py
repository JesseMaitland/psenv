from abc import ABC, abstractmethod
from typing import TypeVar
from .context import Context

StateType = TypeVar('StateType', bound='State')

class State(ABC):

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self._success = False

    @property
    def success(self) -> bool:
        return self._success

    @success.setter
    def success(self, value: bool) -> None:
        self._success = value

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def transition(self) -> StateType:
        pass
