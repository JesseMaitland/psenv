from ramjam.cli import Command


class Pull(Command):


    def __call__(self, *args, **kwargs) -> int:
        print("Pulling")
        return 0

