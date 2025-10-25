from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from postal_oop.items.PostalItem import PostalItem

@dataclass
class Postcard(PostalItem):
    # Для открытки тесты не передают weight_kg/size_cm — даём разумные дефолты
    def __init__(self, tracking_id: str, sender, recipient, stamps_value: float, tariff, weight_kg: float = 0.01, size_cm: Tuple[float, float, float] = (14.0, 9.0, 0.2)):
        super().__init__(tracking_id=tracking_id, sender=sender, recipient=recipient, weight_kg=weight_kg, size_cm=size_cm, stamps_value=stamps_value, tariff=tariff)

    def service_limits(self) -> dict:
        return {
            "max_weight_kg": 0.05,
            "max_lwh_cm": (15.0, 10.0, 0.5),
            "max_girth_plus_length": 50.0,
        }
