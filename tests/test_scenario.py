
import pytest
from core.accounts import SavingsAccount
from core.scenario import Scenario

def test_scenario_creation():

    account1 = SavingsAccount("isa")
    account2 = SavingsAccount("lisa")

    scenario = Scenario()
    scenario.add_account(account1, {"interest_rate": 5, "deposit": 1000})
    scenario.add_account(account2, {"interest_rate": 5, "deposit": 2000})

    assert len(scenario.get_accounts()) == 2

def test_scenario_run():

    account = SavingsAccount("isa")

    scenario = Scenario()
    scenario.add_account(account, {"interest_rate": 5, "deposit": 1000})
    scenario.run(3)

    expected_balance = 0
    for year in range(3):
        expected_balance += 1000
        expected_balance = expected_balance * (1 + 0.05)

    assert scenario.withdraw(100000) == expected_balance