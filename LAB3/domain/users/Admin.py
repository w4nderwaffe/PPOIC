from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
Admin entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Admin:
    userId: int
    permissions: List[str] = field(default_factory=list)
    lastLoginAt: datetime = datetime.utcnow()

    def grantPermission(self, perm: str):
        """Grant a permission string."""
                    if perm not in self.permissions:
                        self.permissions.append(perm)
                    return True

    def revokePermission(self, perm: str):
        """Revoke a permission string."""
                    if perm in self.permissions:
                        self.permissions.remove(perm)
                    return True
