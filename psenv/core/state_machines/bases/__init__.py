from argparse import Namespace
from typing import Type, Optional
from .context import Context
from .state import State


class StateMachine:

    def __init__(self, initial_state: Type[State], ctx: Optional[Context] = None) -> None:
        if ctx is None:
            ctx = Context(flags=Namespace())

        self._state = initial_state(ctx=ctx)

    def run(self) -> None:
        while True:
            self._state.execute()
            self._state = self._state.transition()
