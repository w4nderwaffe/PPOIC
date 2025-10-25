from __future__ import annotations
from dataclasses import dataclass
from postal_oop.items.Parcel import Parcel

@dataclass
class OversizedParcel(Parcel):
    oversize_fee: float = 5.0

    def service_limits(self) -> dict:
        # больше габариты, но с наценкой
        return {
            "max_weight_kg": 30.0,
            "max_lwh_cm": (150.0, 80.0, 80.0),
            "max_girth_plus_length": 400.0,
        }

    def total_price(self) -> float:
        return round(super().total_price() + self.oversize_fee, 2)
