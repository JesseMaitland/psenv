from typing import List, Optional, Dict, Any
import os
import yaml
from pathlib import Path
from psenv.core.error_handling.exceptions import PsenvConfigException
from psenv.environment.config import PSENV_API_CONFIG_FILE
from psenv.utilities.string_utils import string_is_valid

CONFIG_KEYS = (
    "project",
    "prefix",
    "default",
    "environments",
    "environments"
)


class ApiConfig:
    def __init__(self, **kwargs) -> None:
        for key in CONFIG_KEYS:
            if key not in kwargs:
                raise PsenvConfigException(f"Missing required key: {key}")
        self._project = kwargs.get("project")
        self._prefix = kwargs.get("prefix")
        self._default = kwargs.get("default")
        self._environments = kwargs.get("environments")
        self._environment = kwargs.get("environment")

    @property
    def project(self) -> str:
        return self._project

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def default(self) -> str:
        return self._default

    @property
    def environments(self) -> List[str]:
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
                        raise PsenvConfigException(f"Invalid value for key: {key} value: {value} character {char} is not allowed")
        if self.environment not in self.environments:
            raise PsenvConfigException(f"Invalid environment: {self.environment} not in {self.environments}")

class ApiConfigLoader:
    def __init__(self, environment: str, config_file: Optional[Path] = None) -> None:
        self._environment = environment
        self._config_file = config_file or PSENV_API_CONFIG_FILE

    @property
    def environment(self) -> str:
        return self._environment

    @property
    def config_file(self) -> Path:
        return self._config_file

    def read_config(self) -> Dict[str, Any]:
        with open(self.config_file, "r") as f:
            try:
                data = os.path.expandvars(f.read())
                config = yaml.safe_load(data)["psenv"]
            except KeyError:
                raise PsenvConfigException("Missing required root key: 'psenv'")
            except yaml.YAMLError as e:
                raise PsenvConfigException(f"Error loading config file: {e}")
            except FileNotFoundError:
                raise PsenvConfigException(f"Config file not found: {self.config_file}")
            else:
                return config

    def load(self) -> ApiConfig:
        config_dict = self.read_config()
        config = ApiConfig(**config_dict, environment=self.environment)
        config.validate()
        return config
