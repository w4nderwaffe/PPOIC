from __future__ import annotations
from dataclasses import dataclass

"""
Tax entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Tax:
    region: str = ""
    rate: float = 0.0
    inclusive: bool = False

    def compute(self, amount: float):
        """Compute tax for the given amount."""
        return amount * self.rate

    def toggleInclusive(self):
        """Flip inclusive flag."""
        self.inclusive = not self.inclusive
        return self.inclusive