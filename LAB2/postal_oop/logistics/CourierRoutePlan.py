from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from postal_oop.core.PostalAddress import PostalAddress

@dataclass
class CourierRoutePlan:
    courier_id: str
    stops: List[PostalAddress] = field(default_factory=list)

    def add_stop(self, addr: PostalAddress) -> None:
        self.stops.append(addr)

    def next_after(self, addr: PostalAddress) -> Optional[PostalAddress]:
        for i, a in enumerate(self.stops):
            if a.formatted() == addr.formatted():
                return self.stops[i+1] if i+1 < len(self.stops) else None
        return self.stops[0] if self.stops else None

    def total_stops(self) -> int:
        return len(self.stops)
