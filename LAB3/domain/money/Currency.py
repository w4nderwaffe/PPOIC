from __future__ import annotations
from dataclasses import dataclass

"""
Currency entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Currency:
    code: str
    symbol: str = ""
    fractionDigits: int = 2

    def format(self, amount: float):
        """Format amount with symbol."""
        return f"{self.symbol}{amount:.{self.fractionDigits}f}"

    def isSupported(self):
        """Return True if fractionDigits in {0, 2}."""
        return self.fractionDigits in (0, 2)