from psenv.core.state_machines.bases import State


class ExitState(State):

    def execute(self) -> None:
        print('Exiting...')

    def transition(self):
        exit(self.ctx.exit_code)
