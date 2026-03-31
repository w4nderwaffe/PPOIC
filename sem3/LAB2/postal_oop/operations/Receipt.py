from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Receipt:
    id: str
    payment_id: str
    items: List[Tuple[str, float]] = field(default_factory=list)  # (desc, price)
    footer_note: str = "Спасибо за обращение!"

    def add_item(self, description: str, price: float) -> None:
        self.items.append((description, max(0.0, price)))

    def total(self) -> float:
        return round(sum(p for _, p in self.items), 2)

    def render_text(self) -> str:
        lines = [f"RECEIPT #{self.id}", f"PAYMENT: {self.payment_id}", "-"*24]
        for d, p in self.items:
            lines.append(f"{d}: {p:.2f}")
        lines += [ "-"*24, f"TOTAL: {self.total():.2f}", self.footer_note ]
        return "\n".join(lines)
