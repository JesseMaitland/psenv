from abc import ABC
from psenv.core import file_handler
from psenv.bases.paths import Paths


class PathCreator(ABC):

    def __init__(self, paths: Paths) -> None:
        self.paths = paths

    def create_all(self) -> None:
        self.create_directories()
        self.create_files()

    def create_directories(self) -> None:
        for directory in self.paths.directories:
            file_handler.create_dir(directory)

    def create_files(self) -> None:
        for file in self.paths.files:
            file_handler.create_file(file)
