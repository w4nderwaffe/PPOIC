from __future__ import annotations
from dataclasses import dataclass

"""
Shipment entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Shipment:
    id: int
    order: "Order"
    status: str = "CREATED"

    def ship(self):
        """Отгрузить заказ."""
        self.status = "SHIPPED"
        self.order.status = "SHIPPED"
        return True

    def markDelivered(self):
        """Отметить заказ как доставленный."""
        self.status = "DELIVERED"
        self.order.status = "DELIVERED"
        return True