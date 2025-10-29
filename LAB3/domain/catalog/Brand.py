from __future__ import annotations
from dataclasses import dataclass

"""
Brand entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Brand:
    id: int
    name: str
    country: str = ""

    def rename(self, new_name: str):
        """Rename brand."""
        self.name = new_name
        return True

    def verifyBrand(self):
        """Pretend to verify brand."""
        return True