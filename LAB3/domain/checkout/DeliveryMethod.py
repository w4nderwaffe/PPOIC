from __future__ import annotations
from dataclasses import dataclass

"""
DeliveryMethod entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class DeliveryMethod:
    id: int
    name: str
    basePrice: float = 0.0

    def isAvailableForAddress(self, address: "Address"):
        """Доступно, если у адреса указан город."""
        return bool(getattr(address, "city", ""))

    def quote(self, address: "Address"):
        """
        Возвращает стоимость доставки.
        Базовая логика для тестов: basePrice + 0, если есть city, иначе +5.0
        """
        return self.basePrice + (0.0 if getattr(address, "city", "") else 5.0)