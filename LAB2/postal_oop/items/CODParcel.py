from __future__ import annotations
from dataclasses import dataclass
from postal_oop.items.Parcel import Parcel
from postal_oop.exceptions.PaymentDeclinedError import PaymentDeclinedError

@dataclass
class CODParcel(Parcel):
    cod_amount: float = 0.0     # наложенный платёж

    def requires_cod(self) -> bool:
        return self.cod_amount > 0

    def collect_cod(self, paid_amount: float) -> float:
        if not self.requires_cod():
            return 0.0
        if paid_amount + 1e-9 < self.cod_amount:
            raise PaymentDeclinedError(f"Оплачено {paid_amount}, требуется {self.cod_amount}")
        # возврат сдачи
        return round(paid_amount - self.cod_amount, 2)
