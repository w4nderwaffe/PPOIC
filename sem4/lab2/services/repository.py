from models.criteria import DeleteCriteria, SearchCriteria
from models.student_record import StudentRecord


class RecordRepository:
    def __init__(self):
        self._records: list[StudentRecord] = []

    def add(self, record: StudentRecord):
        self._records.append(record)

    def extend(self, records: list[StudentRecord]):
        self._records.extend(records)

    def clear(self):
        self._records.clear()

    def get_all(self) -> list[StudentRecord]:
        return list(self._records)

    def get_groups(self) -> list[str]:
        return sorted({record.group for record in self._records})

    def search(self, criteria: SearchCriteria) -> list[StudentRecord]:
        result = []
        for record in self._records:
            if self._matches(record, criteria):
                result.append(record)
        return result

    def delete(self, criteria: DeleteCriteria) -> int:
        remaining = []
        deleted_count = 0

        for record in self._records:
            if self._matches(record, criteria):
                deleted_count += 1
            else:
                remaining.append(record)

        self._records = remaining
        return deleted_count

    def _matches(self, record: StudentRecord, criteria) -> bool:
        surname = criteria.normalized_surname()
        group = criteria.group
        min_total = criteria.min_total
        max_total = criteria.max_total

        total = record.total_social_work

        surname_match = True
        if surname is not None:
            surname_match = surname in record.surname.lower()

        group_match = True
        if group is not None:
            group_match = record.group == group

        range_match = True
        if min_total is not None:
            range_match = range_match and total >= min_total
        if max_total is not None:
            range_match = range_match and total <= max_total

        has_surname = surname is not None
        has_group = group is not None
        has_range = min_total is not None or max_total is not None

        if has_surname and not has_group and not has_range:
            return surname_match

        if has_group and not has_surname and not has_range:
            return group_match

        if has_surname and has_group and not has_range:
            return surname_match or group_match

        if has_surname and has_range and not has_group:
            return surname_match and range_match

        if has_group and has_range and not has_surname:
            return group_match and range_match

        if has_surname and has_group and has_range:
            return (surname_match or group_match) and range_match

        if not has_surname and not has_group and has_range:
            return range_match

        return True