from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Route:
    id: str
    nodes: List[str]
    zone: str = "national"

    def __init__(self, id: str, nodes: Optional[List[str]] = None, node_ids: Optional[List[str]] = None, zone: str = "national"):
        self.id = id
        self.nodes = node_ids if node_ids is not None else (nodes or [])
        self.zone = zone

    def next_after(self, current_node: str) -> Optional[str]:
        try:
            idx = self.nodes.index(current_node)
        except ValueError:
            return self.nodes[0] if self.nodes else None
        return self.nodes[idx + 1] if idx + 1 < len(self.nodes) else None

    def total_hops(self) -> int:
        return max(0, len(self.nodes) - 1)
