from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from postal_oop.exceptions.AddressInvalidError import AddressInvalidError

@dataclass
class PostalAddress:
    street: str
    house: str
    postal_code: str
    city: str
    country: str
    apartment: Optional[str] = None

    def formatted(self) -> str:
        apt = f", кв. {self.apartment}" if self.apartment else ""
        return f"{self.street}, д. {self.house}{apt}, {self.city}, {self.postal_code}, {self.country}"

    def validate(self) -> None:
        if not (self.street and self.house and self.city and self.country):
            raise AddressInvalidError("Отсутствуют обязательные поля адреса")
        if not self.postal_code.isdigit() or len(self.postal_code) not in (5, 6):
            raise AddressInvalidError("Индекс должен содержать 5–6 цифр")

    def same_city(self, other: "PostalAddress") -> bool:
        return self.city.strip().lower() == other.city.strip().lower()

    def region_hint(self) -> str:
        return (self.country or "").upper() + ":" + (self.postal_code[:2] if self.postal_code else "")
