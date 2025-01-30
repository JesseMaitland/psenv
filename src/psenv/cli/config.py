from ramjam.cli import Command


class Config(Command):
    help = "Generates a psenv configuration file"

    def __call__(self, *args, **kwargs) -> int:
        print("Configuring")
        return 0
