from pydantic import BaseModel
from typing import Dict
"""
aws_accounts:    
    salesforce:
        id: 642165639107
    foobar:
        id: 123456789012
    production:
        id: 123456789012
"""


class AWSAccount(BaseModel):
    id: str

class AWSAccounts(BaseModel):
    aws_accounts: Dict[str, AWSAccount]

    def append_account(self, account_name: str, account_id: str) -> None:
        self.aws_accounts[account_name] = AWSAccount(id=account_id)

    def sort(self) -> None:
        self.aws_accounts = dict(sorted(self.aws_accounts.items()))
