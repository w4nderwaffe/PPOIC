from __future__ import annotations
from dataclasses import dataclass
from postal_oop.logistics.TransportUnit import TransportUnit

@dataclass
class Truck:
    id: str
    plate: str
    unit: TransportUnit
    axle_count: int = 2
    refrigerated: bool = False

    def fuel_needed(self, km: float, consumption_l_per_100km: float = 28.0) -> float:
        base = km * consumption_l_per_100km / 100.0
        return round(base * (1.1 if self.refrigerated else 1.0), 2)
