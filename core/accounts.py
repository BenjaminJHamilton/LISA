


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

        limits = {
            "isa": 20000,
            "lisa": 4000
        }

        if (x > limits[self.type]):
            raise ValueError("Deposit greater than allowed.")


        # add in the govt bonus for lisa
        if (self.type == "lisa"):
            x = x * self.LISA_BONUS
        self.balance += x

    def add_interest(self, rate: float):
        self.balance = self.balance * (1 + rate/100)

    def withdraw(self, house_price: float) -> float:
        
        if (self.type == "lisa" and house_price > 450000):
            return self.balance * self.LISA_PENALTY
        
        return self.balance

        