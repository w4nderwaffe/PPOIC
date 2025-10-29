from __future__ import annotations
from dataclasses import dataclass

"""
CartItem entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class CartItem:
    id: int
    cart: "Cart"
    product: "Product"
    qty: int = 1

    def setQty(self, qty: int):
        """Update quantity (>=1)."""
        self.qty = max(1, int(qty))
        return self.qty