from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict
from .Person import Person

@dataclass
class Customer(Person):
    loyalty_points: int = 0
    preferred_office_id: Optional[str] = None
    preferences: Dict[str, str] = field(default_factory=dict)

    def add_points(self, amount: int) -> None:
        if amount > 0:
            self.loyalty_points += amount

    def set_preference(self, key: str, value: str) -> None:
        self.preferences[key] = value

    def prefers_office(self, office_id: str | None) -> bool:
        # Если передан None — это не «предпочитает этот офис»
        return office_id is not None and self.preferred_office_id == office_id
