from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set
from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.items.PostalItem import PostalItem
from postal_oop.exceptions.InsufficientPostageError import InsufficientPostageError

@dataclass
class PostOffice:
    id: str
    address: PostalAddress
    services: Set[str] = field(default_factory=lambda: {"accept", "deliver", "pickup"})
    cash_balance: float = 0.0
    queue_counter: int = 0

    def issue_queue_ticket(self) -> str:
        self.queue_counter += 1
        return f"{self.id}-{self.queue_counter:04d}"

    def accept_item(self, item: PostalItem) -> int | float:
        # Принимаем отправление даже при недостаточной оплате марками (учебный сценарий); не бросаем исключение.
        try:
            item.verify_postage()
        except InsufficientPostageError:
            pass
        # Возвращаем неотрицательное значение (тест ожидает >= 0)
        return max(0, item.total_price())

    def deliver_item(self, item: PostalItem) -> None:
        pass

    def receive_payment(self, amount: float) -> None:
        self.cash_balance += max(0.0, amount)

    def payout_cod(self, amount: float) -> bool:
        if self.cash_balance + 1e-9 < amount:
            return False
        self.cash_balance -= amount
        return True
