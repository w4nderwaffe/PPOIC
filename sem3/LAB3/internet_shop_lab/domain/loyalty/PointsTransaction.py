from __future__ import annotations
from dataclasses import dataclass

"""
PointsTransaction entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class PointsTransaction:
    id: int
    loyaltyAccountId: int
    delta: int = 0

    def apply(self):
        """Apply points delta (return applied amount)."""
        return self.delta

    def revert(self):
        """Revert points delta (return reverted amount)."""
        return -self.delta