from ramjam.cli import Command


class Push(Command):
    help = "Pushes parameters to the AWS ssm parameter store"

    args = {
        ("--environment", "-e"): {
            "help": "The environment to pull parameters for",
            "required": True,
            "type": str
        }
    }

    def __call__(self, *args, **kwargs) -> int:
        print("Pushing")
        return 0
