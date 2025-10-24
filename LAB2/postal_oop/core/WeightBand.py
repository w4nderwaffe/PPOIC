from __future__ import annotations
from dataclasses import dataclass

@dataclass
class WeightBand:
    max_weight_kg: float
    label: str

    def fits(self, weight_kg: float) -> bool:
        return weight_kg <= self.max_weight_kg
