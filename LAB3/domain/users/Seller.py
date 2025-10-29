from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
Seller entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Seller:
    userId: int
    brand: 'Brand'|None = None
    payoutAccountId: str = ''

    def submitProduct(self, product: 'Product'):
        """Submit a product for listing."""
                    return True

    def requestPayout(self, amount: float):
        """Request seller payout."""
                    return amount > 0.0
