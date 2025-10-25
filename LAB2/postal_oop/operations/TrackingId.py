from __future__ import annotations
from dataclasses import dataclass
from postal_oop.utils import make_id

@dataclass(frozen=True)
class TrackingId:
    code: str

    @staticmethod
    def new(prefix: str = "TRK") -> "TrackingId":
        return TrackingId(code=make_id(prefix).replace("_", "").upper())

    def normalized(self) -> str:
        return self.code.strip().upper()
