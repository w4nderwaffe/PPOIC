from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from postal_oop.logistics.TransportUnit import TransportUnit
from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.exceptions.DeliveryAttemptFailedError import DeliveryAttemptFailedError

@dataclass
class Courier:
    id: str
    unit: TransportUnit
    # тест может передавать full_name — поддерживаем оба
    name: str = "Unknown"
    full_name: Optional[str] = None

    planned_stops: List[str] = field(default_factory=list)
    current_load_kg: float = 0.0
    _cursor: int = 0

    # Делаем unit опциональным через собственный __init__
    def __init__(self, id: str, unit: Optional[TransportUnit] = None,
                 name: str = "Unknown", full_name: Optional[str] = None) -> None:
        self.id = id
        self.unit = unit if unit is not None else TransportUnit(id=f"U-{id}", kind="foot", max_load_kg=30.0)
        self.name = name
        self.full_name = full_name
        if self.full_name and (not self.name or self.name == "Unknown"):
            self.name = self.full_name
        self.planned_stops = []
        self.current_load_kg = 0.0
        self._cursor = 0

    def assign_route(self, stops: List[str]) -> None:
        self.planned_stops = list(stops)
        self._cursor = 0

    def next_stop(self) -> Optional[str]:
        if self._cursor < len(self.planned_stops):
            return self.planned_stops[self._cursor]
        return None

    def advance(self) -> Optional[str]:
        nxt = self.next_stop()
        if nxt is not None:
            self._cursor += 1
        return nxt

    def load(self, weight_kg: float) -> None:
        self.current_load_kg += max(0.0, weight_kg)

    def unload(self, weight_kg: float) -> None:
        self.current_load_kg = max(0.0, self.current_load_kg - max(0.0, weight_kg))

    def attempt_delivery(self, address: PostalAddress, recipient_present: bool) -> None:
        if not recipient_present:
            raise DeliveryAttemptFailedError("Получатель отсутствует")
        return
