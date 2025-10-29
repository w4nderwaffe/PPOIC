from __future__ import annotations
from dataclasses import dataclass
from typing import List

"""
Recommendation entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Recommendation:
    id: int
    customer: "Customer"
    algorithm: str = "popular"

    def generate(self, catalog: List["Product"]):
        """Return top-3 items for demo."""
        return catalog[:3]

    def acceptFeedback(self, score: int):
        """Accept feedback 1..5 (no-op)."""
        return score in range(1, 6)