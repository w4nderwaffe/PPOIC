from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set
from postal_oop.items.AttachmentList import AttachmentList
from postal_oop.exceptions.ProhibitedContentError import ProhibitedContentError

@dataclass
class ProhibitedItemCheck:
    prohibited_keywords: Set[str] = field(default_factory=lambda: {
        "взрывчатка", "аккумулятор", "литий", "газ", "аэрозоль", "оружие", "жидкость>100мл"
    })

    def scan(self, attachments: AttachmentList) -> None:
        kws = attachments.keywords()
        for bad in self.prohibited_keywords:
            if any(bad in kw for kw in kws):
                raise ProhibitedContentError(f"Запрещённый предмет: {bad}")
