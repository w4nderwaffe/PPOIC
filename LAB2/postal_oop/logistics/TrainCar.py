from __future__ import annotations
from dataclasses import dataclass
from postal_oop.logistics.TransportUnit import TransportUnit

@dataclass
class TrainCar:
    id: str
    number: str
    unit: TransportUnit
    gauge_mm: int = 1520

    def axle_load_ok(self) -> bool:
        return self.unit.max_load_kg >= 50_000
