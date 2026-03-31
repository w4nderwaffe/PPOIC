from __future__ import annotations
from dataclasses import dataclass

"""
Payment entity for Internet Shop lab.
This file name equals the class name, per requirement.
"""

@dataclass
class Payment:
    id: int
    order: "Order"
    amount: float = 0.0

    def capture(self, gateway: "PaymentGateway"):
        """Capture funds via gateway; raise if fails."""
        ok = gateway.authorize(self)
        if not ok:
            from exceptions.PaymentCaptureFailedException import PaymentCaptureFailedException
            raise PaymentCaptureFailedException("Capture failed")
        return True

    def void(self):
        """Void payment (no-op)."""
        return True