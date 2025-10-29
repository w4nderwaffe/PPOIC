from __future__ import annotations
from dataclasses import dataclass

"""
Refund entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Refund:
    id: int
    payment: "Payment"
    amount: float = 0.0

    def issue(self):
        """Issue refund; raise if not allowed."""
        if self.amount <= 0:
            from exceptions.RefundNotAllowedException import RefundNotAllowedException
            raise RefundNotAllowedException("Amount must be positive")
        return True

    def cancel(self):
        """Cancel refund (no-op)."""
        return True