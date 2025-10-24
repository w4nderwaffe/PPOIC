from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date

@dataclass
class Stamp:
    code: str
    face_value: float
    country: str
    issued_on: date
    cancelled: bool = field(default=False)

    def cancel(self) -> None:
        self.cancelled = True

    def is_valid_for_country(self, country: str) -> bool:
        return self.country.strip().lower() == country.strip().lower()

    def value_left(self) -> float:
        return 0.0 if self.cancelled else self.face_value
