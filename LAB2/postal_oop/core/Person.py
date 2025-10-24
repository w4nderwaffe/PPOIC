from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Person:
    full_name: str
    id_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    def short_name(self) -> str:
        parts = self.full_name.split()
        if not parts:
            return ""
        fam = parts[0]
        initials = "".join((p[0].upper() + ".") for p in parts[1:3] if p)
        return f"{fam} {initials}".strip()

    def has_contact(self) -> bool:
        return bool(self.phone or self.email)
