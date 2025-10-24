from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.exceptions.OverweightError import OverweightError

@dataclass
class Postbox:
    id: str
    address: PostalAddress
    max_items: int = 50
    max_weight_kg: float = 5.0
    _items_weights: List[float] = field(default_factory=list)

    def can_accept(self, item_weight_kg: float) -> bool:
        if len(self._items_weights) >= self.max_items:
            return False
        if sum(self._items_weights) + item_weight_kg > self.max_weight_kg:
            return False
        return True

    def receive_item(self, item_weight_kg: float) -> None:
        if not self.can_accept(item_weight_kg):
            raise OverweightError("Ящик перегружен (штучно или по весу)")
        self._items_weights.append(item_weight_kg)

    def pickup(self, count: int) -> float:
        count = max(0, min(count, len(self._items_weights)))
        taken = self._items_weights[:count]
        self._items_weights = self._items_weights[count:]
        return sum(taken)

    def load_factor(self) -> float:
        return min(1.0, len(self._items_weights) / self.max_items)
