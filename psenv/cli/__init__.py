from ramjam.cli import Command
from psenv.bases import BasePsenvCommand
from psenv.core import messages
from psenv.core.error_handler import handle_cli_errors
from psenv.core.config import ConfigWriter, ConfigReader

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


class New(BasePsenvCommand):

    args = {
        ("--account", "-a"): {
            "help": "AWS account name and alias",
            "required": False,
            "nargs": 2,
        }
    }

    @handle_cli_errors
    def __call__(self) -> int:

        if self.cli_args.account:
            return self.new_account(*self.cli_args.account)


    def new_account(self, account_name: str, account_id: str) -> int:
        config_reader = ConfigReader(self.project.paths.accounts_file)
        aws_accounts = config_reader.get_aws_accounts()

        if account_name in aws_accounts.aws_accounts:
            print(f"account {account_name} already exists")
            return 1

        aws_accounts.append_account(account_name, account_id)

        config_writer = ConfigWriter(self.project.paths.accounts_file)
        config_writer.write(aws_accounts.model_dump())

        print(f"new account: {account_name} {account_id}")
        return 0
