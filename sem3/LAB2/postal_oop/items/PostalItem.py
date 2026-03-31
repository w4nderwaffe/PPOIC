from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple, List
from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.core.Tariff import Tariff
from postal_oop.core.InsurancePlan import InsurancePlan
from postal_oop.core.Postmark import Postmark
from postal_oop.exceptions.OversizeError import OversizeError
from postal_oop.exceptions.OverweightError import OverweightError
from postal_oop.exceptions.InsufficientPostageError import InsufficientPostageError

@dataclass
class PostalItem:
    tracking_id: str
    sender: PostalAddress
    recipient: PostalAddress
    weight_kg: float
    size_cm: Tuple[float, float, float]
    stamps_value: float
    tariff: Tariff
    insurance_plan: Optional[InsurancePlan] = None
    postmarks: List[Postmark] = field(default_factory=list)
    declared_value: float = 0.0

    def service_limits(self) -> dict:
        return {
            "max_weight_kg": 30.0,
            "max_lwh_cm": (100.0, 60.0, 60.0),
            "max_girth_plus_length": 300.0,
        }

    def _sorted_lwh(self) -> Tuple[float, float, float]:
        l, w, h = self.size_cm
        return tuple(sorted((float(l), float(w), float(h)), reverse=True))

    def check_limits(self) -> None:
        limits = self.service_limits()
        l, w, h = self._sorted_lwh()
        if self.weight_kg - 1e-9 > limits["max_weight_kg"]:
            raise OverweightError(f"Вес {self.weight_kg}кг > лимита {limits['max_weight_kg']}кг")
        L, W, H = limits["max_lwh_cm"]
        if l - 1e-9 > L or w - 1e-9 > W or h - 1e-9 > H:
            raise OversizeError(f"Габариты {self.size_cm} превышают {limits['max_lwh_cm']}")
        girth_plus_length = l + 2 * (w + h)
        if girth_plus_length - 1e-9 > limits["max_girth_plus_length"]:
            raise OversizeError("Периметр + длина превышают лимит")

    def add_postmark(self, mark: Postmark) -> None:
        self.postmarks.append(mark)

    def base_price(self) -> float:
        if not self.tariff:
            return 0.0
        return round(self.tariff.estimate(self.weight_kg), 2)

    def total_price(self) -> float:
        if not self.tariff:
            return 0.0
        base = self.tariff.estimate(self.weight_kg)
        ins = self.insurance_plan.premium(self.declared_value) if self.insurance_plan and self.declared_value > 0 else 0.0
        return round(base + ins, 2)

    def verify_postage(self) -> None:
        required = self.total_price()
        if self.stamps_value + 1e-9 < required:
            raise InsufficientPostageError(f"Оплачено {self.stamps_value}, требуется {required}")
