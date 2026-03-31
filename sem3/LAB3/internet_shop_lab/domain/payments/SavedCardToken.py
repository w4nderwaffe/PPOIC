from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
SavedCardToken entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class SavedCardToken:
    id: int
    customer: 'Customer'
    token: str = ''

    def rotateToken(self):
        """Rotate token value."""
                    self.token = self.token[::-1]
                    return self.token

    def revoke(self):
        """Revoke token (empty)."""
                    self.token = ''
                    return True
