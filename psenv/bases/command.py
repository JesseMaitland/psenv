from ramjam.cli import Command
from psenv.core.project import Project
from psenv.core.error_handler import ErrorHandler

class BasePsenvCommand(Command):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.project = Project()
        self.error_handler = ErrorHandler()
