from typing import Any
from argparse import Namespace
from psenv.core.project import Project

class Context:

    def __init__(self, flags: Namespace, project: Project, **kwargs) -> None:
        self.__dict__.update(kwargs)
        self._exit_code = 0
        self._flags = flags
        self._project = project

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    @property
    def project(self) -> Project:
        return self._project

    @property
    def flags(self) -> Any:
        return getattr(self, '_flags', None)

    @property
    def exit_code(self) -> int:
        return self._exit_code

    @exit_code.setter
    def exit_code(self, value: int) -> None:
        self._exit_code = value

    def get(self, key: str) -> Any:
        return self.__dict__.get(key)

    def set(self, key: str, value: Any) -> None:
        self.__dict__[key] = value
