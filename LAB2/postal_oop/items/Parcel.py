from __future__ import annotations
from dataclasses import dataclass
from postal_oop.items.PostalItem import PostalItem

@dataclass
class Parcel(PostalItem):
    def service_limits(self) -> dict:
        return {
            "max_weight_kg": 20.0,
            "max_lwh_cm": (100.0, 60.0, 60.0),
            "max_girth_plus_length": 300.0,
        }
