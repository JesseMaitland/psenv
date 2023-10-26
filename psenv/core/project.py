from pathlib import Path
from typing import Optional
from psenv.bases import PathCreator, Paths
from psenv.environment.config import PSENV_HOME
from psenv.core.config import ConfigWriter, AWSAccountsConfigReader


class Project:

    def __init__(self) -> None:
        self.paths = ProjectPaths()

    def get_project_creator(self) -> PathCreator:
        return ProjectCreator(self)

    def get_aws_accounts_config_reader(self) -> AWSAccountsConfigReader:
        return AWSAccountsConfigReader(self.paths.accounts_file)



class ProjectPaths(Paths):

    def __init__(self, root: Optional[Path] = None) -> None:
        self._root = root or PSENV_HOME

    @property
    def root(self):
        return self._root

    @property
    def paths_file(self):
        return self.root / 'paths.yml'

    @property
    def accounts_file(self):
        return self.root / 'accounts.yml'

    @property
    def directories(self):
        return [
            self.root,
        ]

    @property
    def files(self):
        return [
            self.paths_file,
            self.accounts_file,
        ]


class ProjectCreator(PathCreator):

    def __init__(self, project: Project) -> None:
        super().__init__(project.paths)
