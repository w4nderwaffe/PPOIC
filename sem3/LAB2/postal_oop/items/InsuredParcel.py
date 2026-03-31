from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Any, Dict
from postal_oop.items.Parcel import Parcel
from postal_oop.items.AttachmentList import AttachmentList

@dataclass
class InsuredParcel(Parcel):
    attachment: Optional[AttachmentList] = field(default=None)

    # Важно: только kwargs — чтобы не ловить конфликт именованных аргументов (insurance).
    def __init__(self, *, attachment: Optional[AttachmentList] = None, **kwargs: Dict[str, Any]) -> None:
        # 1) вычистим потенциальные дубликаты из **base.__dict__
        insurance = kwargs.pop("insurance", None)
        insurance_plan = kwargs.pop("insurance_plan", None)

        # 2) нормализуем в insurance_plan
        if insurance_plan is None and insurance is not None:
            kwargs["insurance_plan"] = insurance
        elif insurance_plan is not None:
            kwargs["insurance_plan"] = insurance_plan

        # 3) вызов родителя
        super().__init__(**kwargs)
        self.attachment = attachment

        # 4) автоподстановка declared_value из декларации, если он не задан
        try:
            if (self.declared_value is None or self.declared_value <= 0) and self.attachment and self.attachment.customs:
                if getattr(self.attachment.customs, "value_eur", 0) > 0:
                    self.declared_value = float(self.attachment.customs.value_eur)
        except Exception:
            # никакой жёсткой зависимости — просто пропускаем
            pass

    def require_insurance(self) -> None:
        if not getattr(self, "insurance_plan", None) or self.declared_value <= 0:
            raise ValueError("Для InsuredParcel нужна страховка и объявленная ценность > 0")
        if not self.insurance_plan.can_cover(self.declared_value):
            raise ValueError("Объявленная ценность превышает покрытие полиса")

    def total_price(self) -> float:
        self.require_insurance()
        return super().total_price()

    def claim_value(self) -> float:
        self.require_insurance()
        return min(self.declared_value, self.insurance_plan.max_cover_value)
