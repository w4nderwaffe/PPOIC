from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from .CustomsDeclaration import CustomsDeclaration

@dataclass
class AttachmentList:
    documents: List[str] = field(default_factory=list)
    customs: Optional[CustomsDeclaration] = None
    items: List[Tuple[str, float]] = field(default_factory=list)

    def add(self, description: str, weight_kg: float) -> None:
        self.items.append((description, max(0.0, weight_kg)))

    def total_weight(self) -> float:
        return round(sum(w for _, w in self.items), 3)

    def keywords(self) -> List[str]:
        kws: List[str] = []
        for desc, _ in self.items:
            kws.extend(desc.lower().split())
        for doc in self.documents:
            kws.extend(str(doc).lower().split())
        return list(dict.fromkeys(kws))
