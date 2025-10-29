from __future__ import annotations
from dataclasses import dataclass

"""
Discount entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Discount:
    id: int
    name: str
    percentage: float = 0.0

    def calculate(self, amount: float):
        """Compute discounted amount."""
        return amount * (1 - self.percentage)

    def isActive(self):
        """Return True if percentage > 0."""
        return self.percentage > 0