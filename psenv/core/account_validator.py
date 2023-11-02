import boto3
from botocore.client import BaseClient
from psenv.core.models import AWSAccount
from psenv.core.exceptions import AccountValidationError


class AccountValidator:

    def __init__(self, account: AWSAccount) -> None:
        self.account = account

    def validate(self) -> None:
        sts = self.get_sts_client()
        account_id = sts.get_caller_identity()["Account"]

        if account_id != self.account.id:
            raise AccountValidationError(
                f"psenv expects account {self.account.id} but account is {account_id}"
            )
        print(f"Using Account: {self.account.id}")

    @staticmethod
    def get_sts_client() -> BaseClient:
        return boto3.client("sts")
