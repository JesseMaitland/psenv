from pathlib import Path
from typing import List, Any, Dict, Optional
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


class ParametersConfigLoader(_BaseConfigLoader):

    def __init__(self, environment: str, config_file: Optional[Path] = None) -> None:
        super().__init__(
            environment=environment,
            config_file=config_file or PSENV_PARAMETERS_CONFIG_FILE,
            config_type=ParametersConfig
        )


__all__ = [
    "ApiConfig",
    "ApiConfigLoader",
    "ParametersConfig",
    "ParametersConfigLoader"
]
