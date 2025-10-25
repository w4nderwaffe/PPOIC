from __future__ import annotations
from dataclasses import dataclass
from postal_oop.items.Letter import Letter

@dataclass
class RegisteredLetter(Letter):
    registration_fee: float = 1.5  # доп. плата за регистрацию

    def total_price(self) -> float:
        return round(super().total_price() + self.registration_fee, 2)
