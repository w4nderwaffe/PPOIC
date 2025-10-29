from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
Coupon entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Coupon:
    code: str
    expiresAt: datetime = datetime.utcnow()
    maxUses: int = 1

    def markUsed(self):
        """Decrement maxUses; raise if exceeded."""

        if self.maxUses <= 0:
            from exceptions.CouponUsageExceededException import CouponUsageExceededException
            raise CouponUsageExceededException("No remaining uses")
        self.maxUses -= 1
        return self.maxUses


    def isValid(self, now: datetime):
        """Check validity vs. expiration."""

        if now > self.expiresAt:
            from exceptions.CouponExpiredException import CouponExpiredException
            raise CouponExpiredException("Coupon expired")
        return self.maxUses > 0

