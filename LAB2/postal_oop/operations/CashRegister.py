from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class CashRegister:
    id: str
    opened: bool = False
    balance: float = 0.0
    payments_log: List[Tuple[str, float, str]] = field(default_factory=list)  # (payment_id, amount, method)

    def open_shift(self, float_amount: float = 0.0) -> None:
        self.opened = True
        self.balance += max(0.0, float_amount)

    def close_shift(self) -> float:
        self.opened = False
        return self.balance

    def accept_payment(self, payment_id: str, amount: float, method: str) -> None:
        if not self.opened:
            raise RuntimeError("Касса закрыта")
        self.balance += max(0.0, amount)
        self.payments_log.append((payment_id, amount, method))

    def refund(self, payment_id: str, amount: float) -> bool:
        if amount > self.balance + 1e-9:
            return False
        self.balance -= amount
        self.payments_log.append((payment_id, -amount, "refund"))
        return True
