from __future__ import annotations
from dataclasses import dataclass

"""
ExchangeRate entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class ExchangeRate:
    baseCode: str
    quoteCode: str
    rate: float = 1.0

    def update(self, new_rate: float):
        """Update internal rate."""
        self.rate = new_rate
        return self.rate

    def convert(self, amount: float):
        """Convert amount using rate."""
        return amount * self.rate