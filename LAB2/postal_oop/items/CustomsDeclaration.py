from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class CustomsDeclaration:
    # Переименовано под тесты: content_description, value_eur, country_of_origin
    content_description: str
    value_eur: float
    country_of_origin: str
    hs_code: Optional[str] = None
    is_document: bool = False

    def requires_declaration(self, international: bool) -> bool:
        if self.is_document:
            return False
        return international and self.value_eur > 0

    def estimate_duties(self, rate_percent: float) -> float:
        return round(self.value_eur * max(0.0, rate_percent) / 100.0, 2)
