from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Set
from postal_oop.domain.DNSRecord import DNSRecord

@dataclass
class Domain:
    """Доменные (территориальные) настройки почтовой сети: страны, узлы, правила."""
    code: str                 # например, "LT", "EU"
    name: str                 # "Lithuania", "European Region"
    offices: Set[str] = field(default_factory=set)        # id отделений
    centers: Set[str] = field(default_factory=set)        # id сортировочных центров
    records: List[DNSRecord] = field(default_factory=list)

    def add_office(self, office_id: str) -> None:
        self.offices.add(office_id)

    def add_center(self, center_id: str) -> None:
        self.centers.add(center_id)

    def add_record(self, rec: DNSRecord) -> None:
        self.records.append(rec)

    def has_office(self, office_id: str) -> bool:
        return office_id in self.offices

    def has_center(self, center_id: str) -> bool:
        return center_id in self.centers

    def find_records(self, prefix: str) -> List[DNSRecord]:
        return [r for r in self.records if r.matches(prefix)]
