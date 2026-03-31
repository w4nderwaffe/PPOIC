from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

"""
Product entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Product:
    id: int
    name: str
    category: "Category" | None = None

    def rename(self, new_name: str):
        """Rename product."""
        self.name = new_name
        return True

    def changeSku(self, new_sku: str):
        """Change SKU (stored as name suffix for demo)."""
        base = self.name.split(" | SKU=")[0]
        self.name = f"{base} | SKU={new_sku}"
        return True