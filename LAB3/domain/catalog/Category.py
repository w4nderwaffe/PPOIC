from __future__ import annotations
from dataclasses import dataclass

"""
Category entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Category:
    id: int
    name: str
    parent: "Category" | None = None

    def moveToParent(self, new_parent: "Category" | None):
        """Reassign parent category."""
        self.parent = new_parent
        return True

    def rename(self, new_name: str):
        """Rename category."""
        self.name = new_name
        return True