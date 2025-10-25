from __future__ import annotations
from dataclasses import dataclass

@dataclass
class TransportUnit:
    id: str
    kind: str                 # 'truck', 'van', 'train', 'air'
    max_load_kg: float
    current_load_kg: float = 0.0
    location_node_id: str = ""

    def can_load(self, weight_kg: float) -> bool:
        return self.current_load_kg + weight_kg <= self.max_load_kg + 1e-9

    def load(self, weight_kg: float) -> None:
        if not self.can_load(weight_kg):
            raise ValueError("Превышение грузоподъёмности")
        self.current_load_kg += weight_kg

    def unload(self, weight_kg: float) -> None:
        self.current_load_kg = max(0.0, self.current_load_kg - weight_kg)
