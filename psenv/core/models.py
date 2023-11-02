from pydantic import BaseModel
from typing import Dict, Optional


class AWSAccount(BaseModel):
    id: str


class AWSAccounts(BaseModel):
    aws_accounts: Dict[str, AWSAccount]

    def append_account(self, account_name: str, account_id: str) -> None:
        self.aws_accounts[account_name] = AWSAccount(id=account_id)

    def sort(self) -> None:
        self.aws_accounts = dict(sorted(self.aws_accounts.items()))

    def get_account(self, account_name: str) -> Optional[AWSAccount]:
        return self.aws_accounts.get(account_name)


"""
environments:
    bi-airflow:
        account: spam # Optional
        ps_path: /services/local-airflow # parameter store path in aws
    
"""

class Environment(BaseModel):
    account: Optional[str]
    ps_path: str

class Environments(BaseModel):
    environments: Dict[str, Environment]

    def append_environment(self, environment_name: str, account_name: str, ps_path: str) -> None:
        self.environments[environment_name] = Environment(account=account_name, ps_path=ps_path)

    def sort(self) -> None:
        self.environments = dict(sorted(self.environments.items()))

    def get_environment(self, environment_name: str) -> Optional[Environment]:
        return self.environments.get(environment_name)
