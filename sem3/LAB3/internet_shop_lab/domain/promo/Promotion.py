from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

"""
Promotion entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Promotion:
    id: int
    title: str
    startsAt: datetime = datetime.utcnow()

    def isRunning(self, now: datetime, endsAt: datetime):
        """Check if promotion is active."""
        return self.startsAt <= now <= endsAt

    def attachProduct(self, product: "Product"):
        """Attach product (no-op)."""
        return True