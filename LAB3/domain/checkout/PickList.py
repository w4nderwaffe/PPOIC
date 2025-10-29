from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
PickList entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class PickList:
    id: int
    warehouse: 'Warehouse'
    createdBy: int = 0

    def addItem(self, item: 'InventoryItem'):
        """Add inventory item (no-op)."""
                    return True

    def markPicked(self):
        """Mark picklist as picked (no-op)."""
                    return True
