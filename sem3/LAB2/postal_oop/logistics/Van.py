from __future__ import annotations
from dataclasses import dataclass
from postal_oop.logistics.TransportUnit import TransportUnit

@dataclass
class Van:
    id: str
    plate: str
    unit: TransportUnit
    doors: int = 4

    def city_efficiency(self, stops: int) -> float:
        return max(0.2, 1.0 - 0.02 * max(0, stops))
