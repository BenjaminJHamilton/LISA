


class SavingsAccount:

    ALLOWED_TYPES = {"isa", "lisa"}
    LISA_BONUS = 1.25
    LISA_PENALTY = 0.75

    def __init__(self, type: str):

        if type not in self.ALLOWED_TYPES:
            raise ValueError(f"Invalid account type '{type}'. Must be one of {self.ALLOWED_TYPES}")

        self.type = type
        self.balance = 0

    def deposit(self, x: float):
        # add in the govt bonus for lisa
        if (self.type == "lisa"):
            x = x * self.LISA_BONUS
        self.balance += x

    def add_interest(self, rate):
        self.balance = self.balance + (1 * rate/100)

    def withdraw(self, house_price):

        if (self.type == "lisa" & house_price > 450000):
            return self.balance * self.LISA_PENALTY
        
        return self.balance