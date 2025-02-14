from collections import defaultdict
from pathlib import Path
from typing import List, Any, Dict, Optional

import yaml

from psenv.core.aws.parameter_store_service import Parameter
from psenv.environment.config import PSENV_API_CONFIG_FILE, PSENV_PARAMETERS_CONFIG_FILE
from psenv.core.configs.bases import _BaseConfig, _BaseConfigLoader


class ApiConfig(_BaseConfig):

    @property
    def environments(self) -> List[str]:
        return self._environments


class ApiConfigLoader(_BaseConfigLoader):

    def __init__(self, environment: str, config_file: Optional[Path] = None) -> None:
        super().__init__(
            environment=environment,
            config_file=config_file or PSENV_API_CONFIG_FILE,
            config_type=ApiConfig
        )


class ParametersConfig(_BaseConfig):

    @property
    def environments(self) -> Dict[str, Any]:
        return self._environments

    @classmethod
    def from_parameters(cls, parameters: List[Parameter]) -> "ParametersConfig":
        environments = defaultdict(lambda: defaultdict(str))

        for p in parameters:
            environments[p.environment][p.env_key] = p.value

        # convert back to normal dict
        environments = {k: dict(v) for k, v in environments.items()}
        return cls(
            project=parameters[0].project,
            prefix=parameters[0].prefix,
            environments=environments,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project": self.project,
            "prefix": self.prefix,
            "environments": self.environments
        }

class ParametersConfigLoader(_BaseConfigLoader):

    def __init__(self, environment: str, config_file: Optional[Path] = None) -> None:
        super().__init__(
            environment=environment,
            config_file=config_file or PSENV_PARAMETERS_CONFIG_FILE,
            config_type=ParametersConfig
        )


class ParametersConfigWriter:

    def __init__(self, config: ParametersConfig, config_file: Optional[Path] = None) -> None:
        self._config = config
        self._config_file = config_file or PSENV_PARAMETERS_CONFIG_FILE

    def write(self) -> None:
        with open(self._config_file, "w") as f:
            yaml.dump(self._config.to_dict(), f, default_flow_style=False, sort_keys=False)

__all__ = [
    "ApiConfig",
    "ApiConfigLoader",
    "ParametersConfig",
    "ParametersConfigLoader",
    "ParametersConfigWriter"

]
