from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from postal_oop.items.PostalItem import PostalItem
from postal_oop.exceptions.SortingError import SortingError

@dataclass
class SortingCenter:
    id: str
    name: str
    capacity: int = 10000
    queue: List[str] = field(default_factory=list)  # tracking_ids

    def enqueue(self, item: PostalItem) -> None:
        if len(self.queue) >= self.capacity:
            raise SortingError("Центр перегружен")
        self.queue.append(item.tracking_id)

    def dequeue(self) -> Optional[str]:
        return self.queue.pop(0) if self.queue else None

    def route_hint(self, item: PostalItem) -> str:
        return item.recipient.region_hint()

    def has_item(self, tracking_id: str) -> bool:
        return tracking_id in self.queue

    def queue_size(self) -> int:
        return len(self.queue)
