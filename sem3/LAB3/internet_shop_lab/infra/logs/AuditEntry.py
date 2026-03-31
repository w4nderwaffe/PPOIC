from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
AuditEntry entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class AuditEntry:
    id: int
    actorId: int
    action: str = ''

    def sign(self):
        """Sign entry (no-op)."""
                    return True

    def verifySignature(self):
        """Verify signature (always True)."""
                    return True
