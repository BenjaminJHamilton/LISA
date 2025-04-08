
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
        self.params = [] # List to hold parameters associated with the each account

    def add_account(self, account: SavingsAccount, params: dict):
        """
        Adds an account to the scenario.

        :param account: The account to be added.
        :param params: Parameters associated with the account. Required keys are 'interest_rate' and 'deposit'.
        :raises ValueError: If any required parameter is missing.
        """

        self._check_params(params)

        self.accounts.append(account)
        self.params.append(params)

        self.history = []  # Initialize history for the scenario
         

    def get_accounts(self) -> List[SavingsAccount]:
        """
        Returns the list of accounts associated with the scenario.

        :return: List of accounts.
        """
        return self.accounts

    def run(self, years: int):
        """
        Runs the scenario by iterating through all accounts and performing actions.
        """
        
        for account_info in zip(self.accounts, self.params):
            account, params = account_info
            account_history = []  # Initialize history for each account

            for year in range(years):
                # Deposit the amount into the account
                account.deposit(params['deposit'])
                # Add interest to the account
                account.add_interest(params['interest_rate'])

                account_history.append(account.balance)  # Store the balance after each year
            
            self.history.append(account_history)  # Store the history for the account

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
    
    def get_history(self) -> List[List[float]]:
        """
        Returns the history of balances for each account.

        :return: List of lists, where each inner list contains the balance history for an account.
        """
        return self.history
    
    def _check_params(self, params: dict):
        """
        Checks if the parameters are valid.

        :param params: Parameters to be checked.
        :raises ValueError: If any parameter is invalid.
        """
        
        required_keys = ['interest_rate', 'deposit']
        
        for key in required_keys:
            if key not in params:
                raise ValueError(f"Missing required parameter: {key}")