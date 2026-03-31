from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
EventLog entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class EventLog:
    id: int
    eventType: str
    createdAt: datetime = datetime.utcnow()

    def attachContext(self, ctx: Dict[str, Any]):
        """Attach context (no-op)."""
                    return True

    def persist(self):
        """Persist (no-op)."""
                    return True
