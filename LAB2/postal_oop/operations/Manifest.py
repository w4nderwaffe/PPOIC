from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .Shipment import Shipment

@dataclass
class Manifest:
    id: str
    route_id: Optional[str] = None
    shipments: Dict[str, Shipment] = field(default_factory=dict)
    shipment_id: Optional[str] = None  # совместимость с тестом
    _entries: List[str] = field(default_factory=list, init=False, repr=False)
    _weight_kg: float = field(default=0.0, init=False, repr=False)

    def add(self, shipment: Shipment) -> None:
        if self.route_id and shipment.route_id and shipment.route_id != self.route_id:
            raise ValueError("Route mismatch: shipment.route_id != manifest.route_id")
        if not self.route_id:
            self.route_id = shipment.route_id
        self.shipments[shipment.id] = shipment

    def add_entry(self, tracking_id: str, weight_kg: float) -> None:
        self._entries.append(tracking_id)
        self._weight_kg += max(0.0, weight_kg)

    def total_items(self) -> int:
        if self.shipments:
            return sum(len(s.item_ids) for s in self.shipments.values())
        return len(self._entries)

    def total_weight(self) -> float:
        if self.shipments:
            return round(sum(s.total_weight_kg for s in self.shipments.values()), 2)
        return round(self._weight_kg, 2)

    def ids(self) -> List[str]:
        if self.shipments:
            return list(self.shipments.keys())
        sid = self.shipment_id or self.id
        return [sid] if self._entries else []

    def has_tracking(self, tracking_id: str) -> bool:
        if self.shipments:
            return any(tracking_id in s.item_ids for s in self.shipments.values())
        return tracking_id in self._entries
