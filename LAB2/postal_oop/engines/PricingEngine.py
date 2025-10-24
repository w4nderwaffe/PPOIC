from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from postal_oop.core.Tariff import Tariff
from postal_oop.core.WeightBand import WeightBand
from postal_oop.core.InsurancePlan import InsurancePlan
from postal_oop.items.PostalItem import PostalItem

@dataclass
class PricingEngine:
    tariffs: List[Tariff] = field(default_factory=list)
    bands: List[WeightBand] = field(default_factory=list)
    default_insurance: Optional[InsurancePlan] = None

    def pick_tariff(self, zone: str, priority: bool) -> Optional[Tariff]:
        # простая стратегия: сначала фильтр по зоне/приоритету, затем с минимальной базой
        candidates = [t for t in self.tariffs if t.zone == zone and (not priority or t.priority)]
        if not candidates:
            candidates = [t for t in self.tariffs if t.zone == zone]
        return min(candidates, key=lambda t: t.base_price) if candidates else None

    def in_band(self, weight_kg: float) -> Optional[WeightBand]:
        fits = [b for b in self.bands if b.fits(weight_kg)]
        return min(fits, key=lambda b: b.max_weight_kg) if fits else None

    def calculate(self, item: PostalItem, zone: str, priority: bool = False, insure: bool = False) -> float:
        tariff = self.pick_tariff(zone, priority)
        if not tariff:
            return 0.0
        base = tariff.estimate(item.weight_kg)
        extra = 0.0
        if insure and self.default_insurance and item.declared_value > 0:
            extra = self.default_insurance.premium(item.declared_value)
        return round(base + extra, 2)
