from rich.console import Console
from rich.table import Table
from psenv.core.models import AWSAccounts


class AccountsTable(Table):

    def __init__(self, aws_accounts: AWSAccounts) -> None:
        super().__init__()
        self.aws_accounts = aws_accounts
        self._add_columns()
        self._add_rows()

    def _add_columns(self) -> None:
        self.add_column('Account Name')
        self.add_column('Account ID')

    def _add_rows(self) -> None:
        for account_name, account in self.aws_accounts.aws_accounts.items():
            self.add_row(account_name, account.id)

    def display(self, console: Console) -> None:
        console.print(self)
