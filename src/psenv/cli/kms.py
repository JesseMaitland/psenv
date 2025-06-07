from ramjam.cli import Command


class Kms(Command):

    help = "Interact with AWS KMS service"

    args = {
        ("action",): {
            "help": "Action to perform",
            "choices": ["create", "delete", "list"],
        }
    }

    def __call__(self) -> int:
        func = getattr(self, self.cliargs.action)
        return func()

    def create(self) -> int:
        print('create')
        return 0

    def delete(self) -> int:
        print('delete')
        return 0

    def list(self) -> int:
        print('list')
        return 0
