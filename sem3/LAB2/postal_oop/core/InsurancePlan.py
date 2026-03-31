from __future__ import annotations
from dataclasses import dataclass

@dataclass
class InsurancePlan:
    code: str
    max_cover_value: float     # максимальная страховая сумма
    price_percent: float       # % от объявленной ценности
    min_price: float = 0.0

    def premium(self, declared_value: float) -> float:
        p = max(self.min_price, declared_value * self.price_percent / 100.0)
        return round(p, 2)

    def can_cover(self, declared_value: float) -> bool:
        return declared_value <= self.max_cover_value
