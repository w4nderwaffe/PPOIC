from __future__ import annotations
from dataclasses import dataclass

"""
SupportTicket entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class SupportTicket:
    id: int
    customer: "Customer"
    status: str = "OPEN"

    def addMessage(self, msg: "ChatMessage"):
        """Attach message (no-op)."""
        return True

    def close(self):
        """Close the ticket."""
        self.status = "CLOSED"
        return True