from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

"""
PasswordPolicy entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class PasswordPolicy:
    minLength: int = 8
    requireSymbol: bool = True
    expireDays: int = 90

    def validate(self, password: str) -> bool:
        """Returns True if password satisfies the policy."""
        if len(password) < self.minLength:
            return False
        if self.requireSymbol and not any(not c.isalnum() for c in password):
            return False
        return True

    def expiresAt(self, from_date: datetime):
        """Returns expiration datetime."""
        return from_date