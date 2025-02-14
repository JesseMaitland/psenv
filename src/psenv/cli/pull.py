from pathlib import Path
from typing import Iterator

from ramjam.cli import Command

from psenv.core.aws.parameter_store_service import ParameterStoreService, Parameter
from psenv.core.configs import ApiConfig, ApiConfigLoader, ParametersConfig, ParametersConfigWriter
from psenv.core.error_handling.error_handler import handle_cli_errors

class Pull(Command):
    help = "Pulls parameters from the AWS ssm parameter store"

    args = {
        ("--environment", "-e"): {
            "help": "The environment to pull parameters for",
            "required": True,
            "type": str,
            "nargs": "*"
        },

        ("--decrypt", "-d"): {
            "help": "Decrypt the parameters",
            "action": "store_true",
            "default": False
        }
    }

    @handle_cli_errors
    def __call__(self) -> int:
        parameters = list(self.pull_parameters())
        parameters_config = ParametersConfig.from_parameters(parameters)
        ParametersConfigWriter(parameters_config).write()
        return 0

    def api_configs(self) -> Iterator[ApiConfig]:
        for env in self.cliargs.environment:
            yield ApiConfigLoader(env).load()

    def ssm_services(self) -> Iterator[ParameterStoreService]:
        for api_config in self.api_configs():
            yield ParameterStoreService(
                path=api_config.ssm_path,
                decrypt=self.cliargs.decrypt
            )

    def pull_parameters(self) -> Iterator[Parameter]:
        for ssm_service in self.ssm_services():
            yield from ssm_service.parameters()

