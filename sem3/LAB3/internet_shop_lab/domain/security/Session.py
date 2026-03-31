from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta

"""
Session entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Session:
    id: int
    userId: int
    expiresAt: datetime
    active: bool = True

    def refresh(self):
        """Продлить сессию на 30 минут и вернуть новую дату истечения."""
        self.expiresAt = datetime.utcnow() + timedelta(minutes=30)
        return self.expiresAt

    def invalidate(self):
        """Деактивировать сессию."""
        self.active = False
        return True