from __future__ import annotations
from dataclasses import dataclass
from postal_oop.items.PostalItem import PostalItem

@dataclass
class Letter(PostalItem):
    def service_limits(self) -> dict:
        # типичные лимиты (примерные; учебные)
        return {
            "max_weight_kg": 0.5,
            "max_lwh_cm": (60.0, 25.0, 5.0),
            "max_girth_plus_length": 90.0,
        }
