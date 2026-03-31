from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from postal_oop.logistics.TransportUnit import TransportUnit

@dataclass
class Shipment:
    id: str
    route_id: str
    unit: TransportUnit
    item_ids: List[str] = field(default_factory=list)
    total_weight_kg: float = 0.0
    departed: bool = False
    arrived: bool = False

    def add_item(self, tracking_id: str, weight_kg: float) -> None:
        if not self.unit.can_load(weight_kg):
            raise ValueError("Нет грузоподъёмности на юните для отправки")
        self.item_ids.append(tracking_id)
        self.unit.load(weight_kg)
        self.total_weight_kg += weight_kg

    def depart(self, from_node_id: str) -> None:
        self.unit.location_node_id = from_node_id
        self.departed = True
        self.arrived = False

    def arrive(self, to_node_id: str) -> None:
        self.unit.location_node_id = to_node_id
        self.arrived = True
        # разгружаем в конце (учебно — суммарно)
        self.unit.unload(self.total_weight_kg)
