from __future__ import annotations
from dataclasses import dataclass

"""
Notification entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Notification:
    id: int
    user: "User"
    channel: str = "email"

    def send(self):
        """Send notification (no-op)."""
        return True

    def markRead(self):
        """Mark notification as read (no-op)."""
        return True