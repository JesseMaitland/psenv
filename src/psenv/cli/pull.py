from ramjam.cli import Command

class Pull(Command):

    help = "Pulls parameters from the AWS ssm parameter store"

    def __call__(self, *args, **kwargs) -> int:
        print("Pulling")
        return 0
