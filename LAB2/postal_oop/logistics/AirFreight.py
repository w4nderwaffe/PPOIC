from __future__ import annotations
from dataclasses import dataclass
from postal_oop.logistics.TransportUnit import TransportUnit

@dataclass
class AirFreight:
    id: str
    flight: str
    unit: TransportUnit
    icao: str = ""

    def iata_label(self) -> str:
        return f"FLT {self.flight}".strip()
