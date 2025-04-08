
from core.accounts import SavingsAccount
from typing import List

class Scenario:
    """
    A class representing a scenario in the simulation.
    """

    def __init__(self):
        """
        Initializes a new Scenario instance.
        """
        
        self.accounts = []  # List to hold accounts associated with the scenario

    def add_account(self, account: SavingsAccount, params: dict):
        """
        Adds an account to the scenario.

        :param account: The account to be added.
        :param params: Parameters associated with the account.
        """

        account_str = {
            "account": account,
            "params": params
        }

        self.accounts.append(account_str)
         

    def get_accounts(self) -> List[SavingsAccount]:
        """
        Returns the list of accounts associated with the scenario.

        :return: List of accounts.
        """
        return self.accounts

    def run(self):
        """
        Runs the scenario by iterating through all accounts and performing actions.
        """
        for account in self.accounts:
            # Perform actions on each account (e.g., deposit, withdraw, etc.)
            pass
            # Placeholder for account actions

    def withdraw(self, house_price: float) -> float:
        """
        Withdraws the specified amount from the accounts.

        :param house_price: The amount to withdraw.
        :return: The total amount withdrawn from all accounts.
        """
        total_withdrawn = 0
        for account in self.accounts:
            total_withdrawn += account.withdraw(house_price)
        return total_withdrawn