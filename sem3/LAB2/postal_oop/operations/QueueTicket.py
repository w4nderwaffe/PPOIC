from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from postal_oop.utils import now

@dataclass
class QueueTicket:
    office_id: str
    number: int
    issued_at: datetime = field(default_factory=now)
    served_at: datetime | None = None

    def code(self) -> str:
        return f"{self.office_id}-{self.number:04d}"

    def mark_served(self) -> None:
        self.served_at = now()

    def wait_time_min(self) -> int:
        end = self.served_at or now()
        return int((end - self.issued_at).total_seconds() // 60)
