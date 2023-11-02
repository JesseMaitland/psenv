from argparse import Namespace
from typing import Dict
from rich.console import Console
from psenv.core.state_machines.bases import State, Context, StateMachine
from psenv.core.state_machines.bases.state import StateType
from psenv.core.state_machines.states import ExitState
from psenv.core.project import Project
from psenv.core.display.accounts_table import AccountsTable
from psenv.core.exceptions import CliArgumentError
from psenv.core import file_handler


class AccountManagerContext(Context):

    def __init__(self, flags: Namespace, project: Project) -> None:
        super().__init__(flags, project)
        self._accounts = None

    @property
    def accounts(self) -> Dict:
        return self._accounts

    @accounts.setter
    def accounts(self, value: Dict) -> None:
        self._accounts = value


class ValidateFlags(State):

    flags = ["new", "update", "delete", "list"]
    forbidden_chars = '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'

    def execute(self) -> None:
        self.validate_action_flags()
        self.validate_aws_account_number()
        self.validate_account_alias()

    def transition(self) -> StateType:
        return LoadAccountFile(self.ctx)

    def validate_action_flags(self) -> None:
        states = [getattr(self.ctx.flags, f, None) is not None for f in self.flags]

        if states.count(True) > 1:
            flags = [f"--{f}" for f in self.flags]
            raise CliArgumentError(f"Only 1 of {flags} may be provided at a time.")

    def validate_aws_account_number(self) -> None:

        aws_account_number = None

        if self.ctx.flags.new:
            aws_account_number = self.ctx.flags.new[1]

        if self.ctx.flags.update:
            aws_account_number = self.ctx.flags.update[1]

        if not self.ctx.flags.delete and not self.ctx.flags.list:
            if not aws_account_number.isdigit():
                raise CliArgumentError(f"An AWS account id only consists of numbers. Received {aws_account_number}")

            if len(aws_account_number) != 12:
                raise CliArgumentError(f"aws account id should be 12 digits. Received only {len(aws_account_number)}")

    def validate_account_alias(self) -> None:

        alias = ""
        if self.ctx.flags.new:
            alias = self.ctx.flags.new[0]

        if self.ctx.flags.update:
            alias = self.ctx.flags.update[0]

        if char := self.forbidden(alias):
            raise CliArgumentError(f"Character {char} is not allowed in alias names.")

    def forbidden(self, value: str) -> str:
        for char in value:
            if char in self.forbidden_chars:
                return char


class SaveAccountFile(State):

    def execute(self) -> None:
        file_handler.write_yml_file(
            path=self.ctx.project.paths.accounts_file,
            content=self.ctx.accounts.model_dump()
        )

    def transition(self) -> StateType:
        return ExitState(self.ctx)


class ListAccount(State):

    def execute(self) -> None:
        console = Console()
        self.ctx.accounts.sort()
        table = AccountsTable(self.ctx.accounts)
        table.display(console)

    def transition(self) -> StateType:
        return ExitState(self.ctx)


class DeleteAccount(State):

    def execute(self) -> None:

        if to_delete := self.remove_entry():
            print(f"removed alias: {self.ctx.flags.delete} account: {to_delete} from accounts config")
        else:
            print(f"account alias {self.ctx.flags.delete} not found.")

    def transition(self) -> StateType:
        if self.success:
            return SaveAccountFile(self.ctx)
        return ExitState(self.ctx)

    def remove_entry(self) -> str:
        if self.ctx.flags.delete in self.ctx.accounts.aws_accounts.keys():
            to_delete = self.ctx.accounts.aws_accounts.pop(self.ctx.flags.delete)
            self.success = True
            return to_delete.id


class UpdateAccount(State):

    def execute(self) -> None:
        account_name, account_id = self.ctx.flags.update

        if account_name in self.ctx.accounts.aws_accounts.keys():
            self.ctx.accounts.append_account(account_name, account_id)
            print(f"Updated account: {account_name} account_id: {account_id} in config")
            self.success = True
        else:
            print(f"Entry not found for account {account_name}. Use the --new flag to add this account to your config.")

    def transition(self) -> StateType:
        if self.success:
            return SaveAccountFile(self.ctx)
        return ExitState(self.ctx)


class NewAccount(State):

    def execute(self) -> None:
        account_name, account_id = self.ctx.flags.new

        if account_name not in self.ctx.accounts.aws_accounts.keys():
            self.ctx.accounts.append_account(account_name, account_id)
            print(f"Added account: {account_name} account_id: {account_id} to config.")
            self.success = True

        else:
            print(f"Entry already exists for account {account_name}. Use the --update or --delete flag to change this.")

    def transition(self) -> StateType:
        if self.success:
            return SaveAccountFile(self.ctx)
        return ExitState(self.ctx)


class LoadAccountFile(State):

    def execute(self) -> None:
        accounts = self.ctx.project.get_aws_accounts_config_reader().get_aws_accounts()
        self.ctx.accounts = accounts

    def transition(self) -> StateType:

        if self.ctx.flags.new:
            return NewAccount(self.ctx)

        if self.ctx.flags.update:
            return UpdateAccount(self.ctx)

        if self.ctx.flags.delete:
            return DeleteAccount(self.ctx)

        if self.ctx.flags.list:
            return ListAccount(self.ctx)


class AccountManager(StateMachine):

    def __init__(self, ctx: AccountManagerContext) -> None:
        super().__init__(
            initial_state=ValidateFlags,
            ctx=ctx
        )
