from __future__ import annotations
from dataclasses import dataclass

"""
Address entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Address:
    id: int
    customer: "Customer" | None = None
    city: str = ""

    def validatePostalCode(self, postal: str):
        """Validate postal code; raise if invalid."""
        if not postal or len(postal) < 4:
            from exceptions.AddressValidationException import AddressValidationException
            raise AddressValidationException("Invalid postal code")
        return True

    def markAsDefault(self, customer: "Customer"):
        """Set this address as default for a customer."""
        customer.defaultAddress = self
        return True