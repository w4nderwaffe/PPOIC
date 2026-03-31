from __future__ import annotations
from dataclasses import dataclass

"""
Customer entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Customer:
    userId: int
    defaultAddress: "Address" | None = None
    loyaltyLevel: int = 0

    def addAddress(self, address: "Address"):
        """Attach an address and optionally set as default."""
        self.defaultAddress = address
        return True

    def upgradeLoyalty(self):
        """Increase loyalty level by 1."""
        self.loyaltyLevel += 1
        return self.loyaltyLevel