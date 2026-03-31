from __future__ import annotations
from dataclasses import dataclass
from typing import List
from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.domain.ServerConfig import ServerConfig  # если понадобится для зон, можно убрать
from postal_oop.logistics.Route import Route

@dataclass
class RoutingEngine:
    def plan(self, source_office_id: str, dest_office_id: str, src: PostalAddress, dst: PostalAddress) -> Route:
        # учебная логика: если города совпадают — локальный маршрут через два узла,
        # иначе — через сортировочный центр "HUB"
        if src.same_city(dst):
            nodes: List[str] = [source_office_id, dest_office_id]
            zone = "local"
        else:
            nodes = [source_office_id, "HUB", dest_office_id]
            zone = "national" if src.country == dst.country else "international"
        return Route(id=f"R_{source_office_id}_{dest_office_id}", nodes=nodes, zone=zone)
