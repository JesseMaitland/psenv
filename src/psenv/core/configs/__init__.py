from typing import List, Any, Dict
from psenv.environment.config import PSENV_API_CONFIG_FILE, PSENV_PARAMETERS_CONFIG_FILE
from psenv.core.configs.bases import __BaseConfig, __BaseConfigLoader


class ApiConfig(__BaseConfig):

    @property
    def environments(self) -> List[str]:
        return self._environments


class ApiConfigLoader(__BaseConfigLoader):

    def __init__(self, environment: str) -> None:
        super().__init__(
            environment=environment,
            config_file=PSENV_API_CONFIG_FILE,
            config_type=ApiConfig
        )


class ParametersConfig(__BaseConfig):

    @property
    def environments(self) -> Dict[str, Any]:
        return self._environments


class ParametersConfigLoader(__BaseConfigLoader):

    def __init__(self, environment: str) -> None:
        super().__init__(
            environment=environment,
            config_file=PSENV_PARAMETERS_CONFIG_FILE,
            config_type=ParametersConfig
        )


__all__ = [
    "ApiConfig",
    "ApiConfigLoader",
    "ParametersConfig",
    "ParametersConfigLoader"
]
