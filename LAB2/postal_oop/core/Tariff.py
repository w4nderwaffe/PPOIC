from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Zone = Literal["local", "regional", "national", "international"]

@dataclass
class Tariff:
    code: str
    name: str
    base_price: float            # базовая стоимость
    price_per_kg: float          # надбавка за кг свыше базового веса
    included_weight_kg: float    # вес, включенный в базу
    zone: Zone                   # зона действия тарифа
    priority: bool = False       # приоритет/экспресс

    def estimate(self, weight_kg: float) -> float:
        extra = max(0.0, weight_kg - self.included_weight_kg)
        return round(self.base_price + extra * self.price_per_kg, 2)

    def is_international(self) -> bool:
        return self.zone == "international"
