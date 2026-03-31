from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Postmark:
    office_id: str
    country: str
    code: str
    stamped_at: datetime

    def to_string(self) -> str:
        return f"{self.country}-{self.office_id}/{self.code} @ {self.stamped_at.isoformat(timespec='seconds')}"

    def is_older_than(self, days: int) -> bool:
        return (datetime.utcnow() - self.stamped_at) > timedelta(days=days)

    def apply_to_text(self, text: str) -> str:
        # Имитация “штемпеля” для печатных форм/квитанций
        return f"{text}\n[POSTMARK {self.to_string()}]"
