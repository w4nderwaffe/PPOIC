from __future__ import annotations
from dataclasses import dataclass

"""
Cart entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Cart:
    id: int
    customer: "Customer"

    def addItem(self, product: "Product", qty: int = 1):
        """Create a CartItem for this cart and product."""
        if qty <= 0:
            qty = 1
        from domain.checkout.CartItem import CartItem
        # deterministic demo id
        return CartItem(id=self.id * 1000 + qty, cart=self, product=product)