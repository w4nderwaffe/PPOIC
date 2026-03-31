from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchCriteria:
    surname: Optional[str] = None
    group: Optional[str] = None
    min_total: Optional[int] = None
    max_total: Optional[int] = None

    def normalized_surname(self) -> Optional[str]:
        if self.surname is None:
            return None
        value = self.surname.strip().lower()
        return value if value else None


@dataclass
class DeleteCriteria:
    surname: Optional[str] = None
    group: Optional[str] = None
    min_total: Optional[int] = None
    max_total: Optional[int] = None

    def normalized_surname(self) -> Optional[str]:
        if self.surname is None:
            return None
        value = self.surname.strip().lower()
        return value if value else None