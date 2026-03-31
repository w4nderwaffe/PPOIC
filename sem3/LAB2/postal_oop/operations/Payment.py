from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Method = Literal["cash", "card", "online"]

@dataclass
class Payment:
    id: str
    amount: float
    currency: str
    method: Method
    approved: bool = False

    def authorize(self) -> None:
        # учебно: авторизуем все суммы > 0
        if self.amount > 0:
            self.approved = True

    def is_cash(self) -> bool:
        return self.method == "cash"
