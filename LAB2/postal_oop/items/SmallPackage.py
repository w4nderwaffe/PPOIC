from __future__ import annotations
from dataclasses import dataclass
from postal_oop.items.Parcel import Parcel

@dataclass
class SmallPackage(Parcel):
    def service_limits(self) -> dict:
        # более строгий лимит, чем у Parcel
        return {
            "max_weight_kg": 2.0,
            "max_lwh_cm": (45.0, 30.0, 30.0),
            "max_girth_plus_length": 120.0,
        }
