from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
GiftCard entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class GiftCard:
    code: str
    balance: float = 0.0
    expiresAt: datetime = datetime.utcnow()

    def redeem(self, amount: float, now: datetime):
        """Redeem if not expired and enough balance."""

        if now > self.expiresAt:
            from exceptions.CouponExpiredException import CouponExpiredException
            raise CouponExpiredException("Gift card expired")
        if amount > self.balance:
            from exceptions.RefundNotAllowedException import RefundNotAllowedException
            raise RefundNotAllowedException("Not enough gift card balance")
        self.balance -= amount
        return self.balance


    def topUp(self, amount: float):
        """Increase balance by amount."""
                    self.balance += max(0.0, amount)
                    return self.balance
