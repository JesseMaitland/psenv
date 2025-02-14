from ramjam.cli import Command
from psenv.factories import ParameterFactory
from psenv.core.error_handling.error_handler import handle_cli_errors
from psenv.core.configs import ParametersConfig, ParametersConfigWriter

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
        pf = ParameterFactory(self.cliargs.environment, self.cliargs.decrypt)
        parameters = pf.list_parameters()
        parameters_config = ParametersConfig.from_parameters(parameters)
        ParametersConfigWriter(parameters_config).write()
        return 0

