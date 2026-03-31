from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
TrackingEvent entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class TrackingEvent:
    id: int
    shipment: 'Shipment'
    status: str = 'CREATED'

    def setTimestamp(self, ts: datetime):
        """No-op set timestamp (not stored, demo)."""
                    return True

    def setNote(self, note: str):
        """No-op set note (not stored, demo)."""
                    return True
