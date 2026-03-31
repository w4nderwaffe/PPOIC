from __future__ import annotations
from dataclasses import dataclass
from postal_oop.items.Parcel import Parcel

@dataclass
class FragileParcel(Parcel):
    fragile_fee: float = 2.0

    def total_price(self) -> float:
        return round(super().total_price() + self.fragile_fee, 2)

    def handling_note(self) -> str:
        return "Осторожно: Хрупкое"
