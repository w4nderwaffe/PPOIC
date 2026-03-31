from __future__ import annotations
from dataclasses import dataclass

"""
SMSMessage entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class SMSMessage:
    id: int
    toNumber: str
    text: str = ""

    def truncateIfNeeded(self, limit: int = 160):
        """Truncate text to limit."""
        self.text = self.text[:limit]
        return self.text

    def dispatch(self):
        """Dispatch SMS (no-op)."""
        return True