from pathlib import Path
from typing import Any, Dict
from psenv.core.models import AWSAccount, AWSAccounts
from psenv.core import file_handler


class ConfigReader:

        def __init__(self, path: Path) -> None:
            self.path = path

        def read(self) -> Dict[str, Any]:
            return file_handler.read_yml_file(self.path)

        def get_aws_accounts(self) -> AWSAccounts:
            config = self.read()
            if config:
                return AWSAccounts(**config)
            return AWSAccounts(aws_accounts={})

class ConfigWriter:

    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, content: dict) -> None:
        file_handler.write_yml_file(self.path, content)
