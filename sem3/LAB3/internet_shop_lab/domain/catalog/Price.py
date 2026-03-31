from __future__ import annotations
from dataclasses import dataclass

"""
Price entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Price:
    product: "Product"
    amount: float = 0.0
    currency: "Currency" = None  # type: ignore

    def convertTo(self, target: "Currency", rate: "ExchangeRate"):
        """Convert price using provided rate."""
        return Price(product=self.product, amount=rate.convert(self.amount), currency=target)

    def applyDiscountAmount(self, value: float):
        """Apply absolute discount (not below zero)."""
        self.amount = max(0.0, self.amount - max(0.0, value))
        return self.amount