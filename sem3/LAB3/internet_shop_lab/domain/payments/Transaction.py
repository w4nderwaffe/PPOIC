from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
Transaction entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Transaction:
    id: int
    payment: 'Payment'
    status: str = 'PENDING'

    def markSuccess(self):
        """Mark transaction successful."""
                    self.status = 'SUCCESS'
                    return True

    def markFailed(self):
        """Mark transaction failed."""
                    self.status = 'FAILED'
                    return True
