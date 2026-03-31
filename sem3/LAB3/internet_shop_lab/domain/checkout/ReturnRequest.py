from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
ReturnRequest entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class ReturnRequest:
    id: int
    order: 'Order'
    reason: str = ''

    def approve(self):
        """Approve return request (no-op)."""
                    return True

    def decline(self):
        """Decline return request (no-op)."""
                    return True
