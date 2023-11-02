from argparse import Namespace
from typing import Dict
from psenv.core.state_machines.bases import State, Context, StateMachine
from psenv.core.project import Project
from psenv.core.exceptions import CliArgumentError
from psenv.core.state_machines.bases.state import StateType
from psenv.core.state_machines.states import ExitState


class EnvironmentManagerContext(Context):

    def __init__(self, flags: Namespace, project: Project) -> None:
        super().__init__(flags, project)
        self._environments = None

    @property
    def environments(self) -> Dict:
        return self._environments

    @environments.setter
    def environments(self, value: Dict) -> None:
        self._environments = value


class ValidateFlags(State):
    flags = ["new", "update", "delete", "list"]
    forbidden_chars = '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'

    def execute(self) -> None:
        self.validate_action_flags()
        self.validate_environment_name()

    def transition(self) -> StateMachine:
        return LoadEnvironmentFile(self.ctx)

    def validate_action_flags(self) -> None:
        states = [getattr(self.ctx.flags, f, None) is not None for f in self.flags]

        if states.count(True) > 1:
            flags = [f"--{f}" for f in self.flags]
            raise CliArgumentError(f"Only 1 of {flags} may be provided at a time.")

    def validate_environment_name(self) -> None:

        environment_name = None

        if self.ctx.flags.new:
            environment_name = self.ctx.flags.new[1]

        if self.ctx.flags.update:
            environment_name = self.ctx.flags.update[1]

        if not self.ctx.flags.delete and not self.ctx.flags.list:
            if not environment_name.isalnum():
                raise CliArgumentError(
                    f"An environment name can only contain alphanumeric characters. Received {environment_name}")


class SaveEnvironmentFile(State):

    def execute(self) -> None:
        print("SaveEnvironmentFile")

    def transition(self) -> StateType:
        return ExitState(self.ctx)


class ListEnvironments(State):

    def execute(self) -> None:
        print("ListEnvironments")

    def transition(self) -> StateType:
        return ExitState(self.ctx)


class DeleteEnvironment(State):

    def execute(self) -> None:
        print("DeleteEnvironment")

    def transition(self) -> StateType:
        if self.success:
            return SaveEnvironmentFile(self.ctx)
        return ExitState(self.ctx)


class UpdateEnvironment(State):

    def execute(self) -> None:
        print("UpdateEnvironment")

    def transition(self) -> StateType:
        if self.success:
            return SaveEnvironmentFile(self.ctx)
        return ExitState(self.ctx)


class NewEnvironment(State):

    def execute(self) -> None:
        print('NewEnvironment')

    def transition(self) -> StateType:
        if self.success:
            return SaveEnvironmentFile(self.ctx)
        return ExitState(self.ctx)


class LoadEnvironmentFile(State):

    def execute(self) -> None:
        environments = self.ctx.project.get_environments_config_reader().get_environments()
        self.ctx.environments = environments

    def transition(self) -> StateType:

        if self.ctx.flags.new:
            return NewEnvironment(self.ctx)

        if self.ctx.flags.update:
            return UpdateEnvironment(self.ctx)

        if self.ctx.flags.delete:
            return DeleteEnvironment(self.ctx)

        if self.ctx.flags.list:
            return ListEnvironments(self.ctx)
