from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional
from postal_oop.core.PostalAddress import PostalAddress
from postal_oop.exceptions.LockerOccupiedError import LockerOccupiedError
from postal_oop.exceptions.OverweightError import OverweightError

@dataclass
class Locker:
    id: str
    location: PostalAddress
    max_weight_per_cell_kg: float = 20.0
    cells: Dict[str, Optional[str]] = field(default_factory=dict)  # cell_id -> tracking_id|None

    def add_cell(self, cell_id: str) -> None:
        if cell_id not in self.cells:
            self.cells[cell_id] = None

    def is_free(self, cell_id: str) -> bool:
        return self.cells.get(cell_id) is None

    def reserve(self, cell_id: str, tracking_id: str) -> None:
        if not self.is_free(cell_id):
            raise LockerOccupiedError(f"Ячейка {cell_id} занята")
        self.cells[cell_id] = tracking_id

    def put(self, cell_id: str, tracking_id: str, weight_kg: float) -> None:
        if weight_kg > self.max_weight_per_cell_kg + 1e-9:
            raise OverweightError("Превышение веса для ячейки")
        self.reserve(cell_id, tracking_id)

    def pickup(self, cell_id: str) -> Optional[str]:
        tid = self.cells.get(cell_id)
        self.cells[cell_id] = None
        return tid
