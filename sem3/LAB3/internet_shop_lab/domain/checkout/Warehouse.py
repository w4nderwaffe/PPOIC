from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
Warehouse entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Warehouse:
    id: int
    name: str
    location: str = ''

    def allocate(self, item: 'InventoryItem', qty: int):
        """Allocate inventory."""
                    item.decreaseStock(qty)
                    return True

    def deallocate(self, item: 'InventoryItem', qty: int):
        """Return inventory."""
                    item.increaseStock(qty)
                    return True
