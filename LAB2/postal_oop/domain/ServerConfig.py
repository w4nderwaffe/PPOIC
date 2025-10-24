from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set
from postal_oop.domain.Domain import Domain

@dataclass
class ServerConfig:
    """Конфигурация почтовой сети/узла."""
    domain: Domain
    hub_id: str                              # главный сортировочный центр
    allowed_zones: Set[str] = field(default_factory=lambda: {"local","regional","national","international"})

    def is_local_route(self, src_city: str, dst_city: str) -> bool:
        return src_city.strip().lower() == dst_city.strip().lower()

    def zone_for(self, src_country: str, dst_country: str, same_city: bool) -> str:
        if same_city:
            return "local"
        return "national" if src_country.strip().lower() == dst_country.strip().lower() else "international"

    def knows_office(self, office_id: str) -> bool:
        return self.domain.has_office(office_id)

    def hub(self) -> str:
        return self.hub_id
