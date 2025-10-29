from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
PaymentCard entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class PaymentCard:
    id: int
    customer: 'Customer'
    maskedPan: str = '****'

    def setDefault(self, customer: 'Customer'):
        """Set this card as default (attach to customer)."""
                    customer.defaultAddress = customer.defaultAddress
                    return True

    def expire(self):
        """Expire card (mask)."""
                    self.maskedPan = 'EXPIRED'
                    return True
