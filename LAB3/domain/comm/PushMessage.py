from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any

"""
PushMessage entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class PushMessage:
    id: int
    deviceToken: str
    payload: Dict[str, Any] = field(default_factory=dict)

    def enrichPayload(self, extra: Dict[str, Any]):
        """Merge extra into payload."""
        self.payload.update(extra)
        return self.payload

    def dispatch(self):
        """Dispatch push (no-op)."""
        return True