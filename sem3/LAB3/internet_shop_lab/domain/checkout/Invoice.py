from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
Invoice entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Invoice:
    id: int
    order: 'Order'
    total: float = 0.0

    def generatePdf(self):
        """Pretend to generate PDF and return bytes."""
                    return b'%PDF-FAKE'

    def markSent(self):
        """Mark invoice as sent (no-op)."""
                    return True
