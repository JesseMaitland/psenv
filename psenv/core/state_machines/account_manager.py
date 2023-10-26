from argparse import Namespace
from typing import Dict
from psenv.core.state_machines.bases import State, Context, StateMachine
from psenv.core.state_machines.bases.state import StateType
from psenv.core.state_machines.states import ExitState
from psenv.core.project import Project


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

    def execute(self) -> None:
        print("ValidateFlags")

    def transition(self) -> StateType:
        return LoadAccountFile(self.ctx)


class SaveAccountFile(State):

    def execute(self) -> None:
        print("SaveAccountFile")

    def transition(self) -> StateType:
        return ExitState(self.ctx)


class ListAccount(State):

    def execute(self) -> None:
        print(self.ctx.accounts)

    def transition(self) -> StateType:
        return ExitState(self.ctx)


class DeleteAccount(State):

    def execute(self) -> None:
        print("DeleteAccount")

    def transition(self) -> StateType:
        return SaveAccountFile(self.ctx)


class UpdateAccount(State):

    def execute(self) -> None:
        print("UpdateAccount")

    def transition(self) -> StateType:
        return SaveAccountFile(self.ctx)


class NewAccount(State):

    def execute(self) -> None:
        print("NewAccount")

    def transition(self) -> StateType:
        return SaveAccountFile(self.ctx)


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
