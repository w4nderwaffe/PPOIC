from __future__ import annotations
from dataclasses import dataclass

"""
ChatMessage entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class ChatMessage:
    id: int
    ticket: "SupportTicket"
    authorId: int = 0

    def redactPII(self, text: str):
        """Redact naive PII (digits → #)."""
        return "".join("#" if ch.isdigit() else ch for ch in text)

    def edit(self, new_text: str):
        """Edit message (no-op)."""
        return True