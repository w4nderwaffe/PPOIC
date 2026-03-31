from __future__ import annotations
from dataclasses import dataclass

"""
Wishlist entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Wishlist:
    id: int
    customer: "Customer"
    name: str = "Default"

    def addProduct(self, product: "Product"):
        """Add product (no-op)."""
        return True

    def removeProduct(self, product: "Product"):
        """Remove product (no-op)."""
        return True