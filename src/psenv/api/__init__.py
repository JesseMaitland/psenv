import os
from pathlib import Path
from typing import Optional

from psenv.core.configs import ApiConfig, ApiConfigLoader
from psenv.core.aws import ParameterStoreService

PSENV_PARAMETER_PATH = os.getenv("PSENV_PARAMETER_PATH")
PSENV_API_CONFIG_PATH = Path(os.getenv("PSENV_API_CONFIG_PATH"))
PSENV_API_ENVIRONMENT = os.getenv("PSENV_API_ENVIRONMENT")


class LoadPsEnv:

    def __init__(self, ssm_path: Optional[str] = None, env: Optional[str] = None, config_path: Optional[Path] = None) -> None:
        self._env = env or PSENV_API_ENVIRONMENT
        self._ssm_path = ssm_path or PSENV_PARAMETER_PATH
        self._config_path = config_path or PSENV_API_CONFIG_PATH

        if self._ssm_path and self._env:
            raise ValueError("Only one of environment or ssm path can be provided")

        if not self._ssm_path and not self._env:
            raise ValueError("Either environment or ssm path must be provided")

        


    def __call__(self) -> None:
        ssm_path = self._get_ssm_path()
        service = ParameterStoreService(path=ssm_path, decrypt=True)
        for parameter in service.parameters():
            os.environ[parameter.parameter_env_key] = parameter.value

    @property
    def _config_loader_kwargs(self) -> dict:
        kwargs = {}
        if PSENV_API_CONFIG_PATH:
            kwargs["config_file"] = PSENV_API_CONFIG_PATH
        kwargs["environment"] = self._env
        return kwargs

    def _get_ssm_path(self) -> str:
        if self._ssm_path:
            return self._ssm_path

        loader = ApiConfigLoader(**self._config_loader_kwargs)
        config = loader.load()
        return config.ssm_path


__all__ = [
    "LoadPsEnv",
    "ApiConfig",
    "ApiConfigLoader",
]
