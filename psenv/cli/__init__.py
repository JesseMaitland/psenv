from ramjam.cli import Command
from psenv.bases import BasePsenvCommand
from psenv.core import messages
from psenv.core.error_handler import handle_cli_errors
from psenv.core.config import ConfigWriter, ConfigReader
from psenv.core.state_machines.account_manager import AccountManager, AccountManagerContext

__version__ = "0.17.1"


class Version(Command):

    def __call__(self) -> int:
        print(f"psenv :: version {__version__}")
        return 0


class Init(BasePsenvCommand):

    @handle_cli_errors
    def __call__(self) -> int:
        return self.initialize()

    def initialize(self) -> int:
        project_creator = self.project.get_project_creator()
        project_creator.create_all()
        messages.project_initialized(self.project.paths.root)
        return 0


class Account(BasePsenvCommand):
    args = {

        ("--new", "-n"): {
            "help": "Create a new account",
            "required": False,
            "default": False,
            "nargs": 2,
        },

        ("--update", "-u"): {
            "help": "Update an existing account",
            "required": False,
            "default": False,
            "nargs": 2,
        },

        ("--delete", "-d"): {
            "help": "Delete an account",
            "required": False,
            "default": False,
        },

        ("--list", "-l"): {
            "help": "List all accounts",
            "required": False,
            "default": False,
            "action": "store_true",
        }
    }

    @handle_cli_errors
    def __call__(self) -> int:
        ctx = AccountManagerContext(
            flags=self.cli_args,
            project=self.project
        )
        account_manager = AccountManager(ctx)
        account_manager.run()
        return ctx.exit_code
