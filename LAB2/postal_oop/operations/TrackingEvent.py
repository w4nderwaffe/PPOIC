from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional
from postal_oop.utils import now

Status = Literal[
    "CREATED", "ACCEPTED", "SORTED", "IN_TRANSIT",
    "OUT_FOR_DELIVERY", "DELIVERED", "ATTEMPTED", "RETURNED"
]

@dataclass
class TrackingEvent:
    tracking_id: str
    status: Status
    location_node_id: str
    timestamp: datetime = None
    note: Optional[str] = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = now()

    def as_dict(self) -> dict:
        return {
            "tracking_id": self.tracking_id,
            "status": self.status,
            "location": self.location_node_id,
            "timestamp": self.timestamp.isoformat(),
            "note": self.note,
        }

    def is_final(self) -> bool:
        return self.status in ("DELIVERED", "RETURNED")
