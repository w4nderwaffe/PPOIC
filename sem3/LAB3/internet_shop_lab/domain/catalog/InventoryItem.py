from __future__ import annotations
from dataclasses import dataclass

"""
InventoryItem entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class InventoryItem:
    id: int
    product: "Product"
    quantity: int = 0

    def increaseStock(self, delta: int):
        """Increase stock by delta."""
        self.quantity += max(0, delta)
        return self.quantity

    def decreaseStock(self, delta: int):
        """Decrease stock; raise if insufficient."""
        if delta < 0:
            delta = -delta
        if self.quantity < delta:
            from exceptions.InsufficientInventoryException import InsufficientInventoryException
            raise InsufficientInventoryException("Not enough stock")
        self.quantity -= delta
        return self.quantity