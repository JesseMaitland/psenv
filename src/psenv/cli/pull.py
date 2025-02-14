from pathlib import Path

from ramjam.cli import Command

from psenv.core.aws.parameter_store_service import ParameterStoreService
from psenv.core.configs import ApiConfig, ApiConfigLoader
from psenv.core.error_handling.error_handler import handle_cli_errors

class Pull(Command):
    help = "Pulls parameters from the AWS ssm parameter store"

    args = {
        ("--environment", "-e"): {
            "help": "The environment to pull parameters for",
            "required": True,
            "type": str
        },

        ("--decrypt", "-d"): {
            "help": "Decrypt the parameters",
            "action": "store_true",
            "default": False
        }
    }

    @handle_cli_errors
    def __call__(self) -> int:
        config = self.get_config()
        ssm_service = self.get_ssm_service(config)

        for parameter in ssm_service.parameters():
            print(parameter)
        return 0

    def get_config(self) -> ApiConfig:
        return ApiConfigLoader(config_file=Path("demo/psenv.yml"),
        environment=self.cliargs.environment).load()

    def get_ssm_service(self, config: ApiConfig) -> ParameterStoreService:
        return ParameterStoreService(
            path=config.ssm_path,
            decrypt=self.cliargs.decrypt
        )
