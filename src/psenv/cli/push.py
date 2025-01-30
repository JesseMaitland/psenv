from ramjam.cli import Command


class Push(Command):
    help = "Pushes parameters to the AWS ssm parameter store"

    def __call__(self, *args, **kwargs) -> int:
        print("Pushing")
        return 0
