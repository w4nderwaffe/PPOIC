from __future__ import annotations
from dataclasses import dataclass

"""
Wallet entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Wallet:
    id: int
    customer: "Customer"
    balance: float = 0.0

    def deposit(self, amount: float):
        """Increase balance by amount."""
        self.balance += max(0.0, amount)
        return self.balance

    def withdraw(self, amount: float):
        """Decrease balance; raise if insufficient."""
        if amount > self.balance:
            from exceptions.PaymentAuthorizationFailedException import PaymentAuthorizationFailedException
            raise PaymentAuthorizationFailedException("Insufficient funds")
        self.balance -= amount
        return self.balance