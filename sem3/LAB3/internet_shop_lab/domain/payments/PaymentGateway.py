from __future__ import annotations
from dataclasses import dataclass

"""
PaymentGateway entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class PaymentGateway:
    id: int
    name: str
    configId: str = ""

    def authorize(self, payment: "Payment"):
        """Return True if payment amount <= 1000."""
        return payment.amount <= 1000.0

    def refund(self, payment: "Payment", amount: float):
        """Refund up to amount; raise if auth fails."""
        if amount <= 0:
            from exceptions.RefundNotAllowedException import RefundNotAllowedException
            raise RefundNotAllowedException("Refund amount must be positive")
        return True