from pathlib import Path
from typing import Optional
from psenv.bases import PathCreator, Paths
from psenv.environment.config import PSENV_HOME
from psenv.core.config import AWSAccountsConfigReader, EnvironmentsConfigReader
from psenv.core.account_validator import AccountValidator


class Project:

    def __init__(self) -> None:
        self.paths = ProjectPaths()

    def get_project_creator(self) -> PathCreator:
        return ProjectCreator(self)

    def get_aws_accounts_config_reader(self) -> AWSAccountsConfigReader:
        return AWSAccountsConfigReader(self.paths.accounts_file)

    def get_environments_config_reader(self) -> EnvironmentsConfigReader:
        return EnvironmentsConfigReader(self.paths.environments_file)

    def get_account_validator(self, account_name: str) -> AccountValidator:
        config_reader = self.get_aws_accounts_config_reader()
        accounts = config_reader.get_aws_accounts()

        return AccountValidator(
            account=accounts.get_account(account_name)
        )

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
    def environments_file(self):
        return self.root / 'environments.yml'

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
            self.environments_file
        ]


class ProjectCreator(PathCreator):

    def __init__(self, project: Project) -> None:
        super().__init__(project.paths)
