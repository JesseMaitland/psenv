from argparse import Namespace
from typing import Type, Optional
from psenv.core.project import Project
from .context import Context
from .state import State


class StateMachine:

    def __init__(self, initial_state: Type[State], ctx: Optional[Context] = None) -> None:
        if ctx is None:
            ctx = Context(flags=Namespace(), project=Project())

        self._state = initial_state(ctx=ctx)


    def run(self) -> None:
        while True:
            self._state.success = False
            self._state.execute()
            self._state = self._state.transition()
