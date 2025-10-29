from __future__ import annotations
from dataclasses import dataclass
from typing import List

"""
Order entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Order:
    id: int
    customer: "Customer"
    status: str = "NEW"

    def place(self, items: List["OrderItem"]):
        """Place order; mark as PLACED."""
        self.status = "PLACED"
        return True

    def cancel(self):
        """Cancel unless already shipped (raise otherwise)."""
        if self.status == "SHIPPED":
            from exceptions.OrderAlreadyShippedException import OrderAlreadyShippedException
            raise OrderAlreadyShippedException("Order already shipped")
        self.status = "CANCELLED"
        return True