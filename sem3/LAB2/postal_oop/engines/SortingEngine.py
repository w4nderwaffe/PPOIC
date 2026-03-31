from __future__ import annotations
from dataclasses import dataclass
from typing import List
from postal_oop.items.PostalItem import PostalItem

@dataclass
class SortingEngine:
    def choose_center(self, item: PostalItem, centers: List[str]) -> str:
        # грубо: берём центр по префиксу региона (страна:индекс[:2])
        hint = item.recipient.region_hint()
        if not centers:
            return "HUB"
        # детерминированный выбор для повторяемости
        idx = abs(hash(hint)) % len(centers)
        return centers[idx]

    def barcode_ok(self, tracking_code: str) -> bool:
        # простой контроль длины/алфавита
        return tracking_code.isalnum() and 8 <= len(tracking_code) <= 32
