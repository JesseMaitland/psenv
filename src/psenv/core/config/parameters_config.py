from typing import List, Dict, Any

from psenv.core.error_handling.exceptions import PsenvConfigException
from psenv.utilities.string_utils import string_is_valid

CONFIG_KEYS = (
    "project",
    "prefix",
    "environments"
    "environment"
)


#TODO: make a base config class as this is basically the same as the ApiConfig class
class ParametersConfig:

    def __init__(self, **kwargs) -> None:
        for key in CONFIG_KEYS:
            if key not in kwargs:
                raise PsenvConfigException(f"Missing required key: {key}")
        self._project = kwargs.get("project")
        self._prefix = kwargs.get("prefix")
        self._environments = kwargs.get("environments")
        self._environment = kwargs.get("environment")

    @property
    def project(self) -> str:
        return self._project

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def environments(self) -> Dict[str, Any]:
        return self._environments

    @property
    def environment(self) -> str:
        return self._environment

    @property
    def ssm_path(self) -> str:
        return f"/{self.prefix}/{self.project}/{self.environment}"

    def validate(self) -> None:
        for key in CONFIG_KEYS:
            value = getattr(self, key)
            if isinstance(value, str):
                if char := string_is_valid(value):
                    raise PsenvConfigException(f"Invalid value for key: {key} value: {value} character {char} is not allowed")
            elif isinstance(value, list):
                for item in value:
                    if char := string_is_valid(item):
                        raise PsenvConfigException(f"Invalid value for key: {key} value: {item} character {char} is not allowed")
