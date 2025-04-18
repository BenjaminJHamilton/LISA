
import pytest
from core.accounts import SavingsAccount

def test_account_creation():
    # Check only isa or lisa are allowed
    account = SavingsAccount("isa")
    account = SavingsAccount("lisa")

    with pytest.raises(ValueError):
        account = SavingsAccount("pension")

def test_deposit():

    account = SavingsAccount("isa")
    assert account.balance == 0
    account.deposit(1000)
    assert account.balance == 1000

def test_lisa_deposit():

    account = SavingsAccount("lisa")
    account.deposit(1000)

    assert account.balance == 1000 * 1.25

def test_account_withdraw():
    account = SavingsAccount("isa")
    account.deposit(1000)
    assert account.withdraw(100000) == 1000

def test_interest():
    account = SavingsAccount("isa")
    account.deposit(1000)
    account.add_interest(5)
    assert account.balance == 1000 * (1 + 5/100)
    account.deposit(1000)
    account.add_interest(5)
    assert account.balance == (1000 * (1 + 5/100) + 1000) * (1 + 5/100)
