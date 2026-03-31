from models.criteria import DeleteCriteria, SearchCriteria
from models.student_record import StudentRecord
from services.repository import RecordRepository


def make_record(full_name, group, values):
    return StudentRecord(full_name=full_name, group=group, social_work=values)


def make_repository():
    repository = RecordRepository()
    repository.extend([
        make_record("Иванов Иван Иванович", "ПИ-21", [1] * 10),
        make_record("Петров Петр Петрович", "ПИ-22", [2] * 10),
        make_record("Сидоров Сидор Сидорович", "ПИ-21", [3] * 10),
    ])
    return repository


def test_repository_add_and_get_all():
    repository = RecordRepository()
    record = make_record("Иванов Иван Иванович", "ПИ-21", [1] * 10)

    repository.add(record)

    assert repository.get_all() == [record]


def test_repository_clear():
    repository = make_repository()

    repository.clear()

    assert repository.get_all() == []


def test_repository_get_groups_returns_sorted_unique_groups():
    repository = make_repository()

    assert repository.get_groups() == ["ПИ-21", "ПИ-22"]


def test_repository_search_by_surname():
    repository = make_repository()

    result = repository.search(SearchCriteria(surname="иванов"))

    assert len(result) == 1
    assert result[0].surname == "Иванов"


def test_repository_search_by_group():
    repository = make_repository()

    result = repository.search(SearchCriteria(group="ПИ-21"))

    assert len(result) == 2


def test_repository_search_by_surname_or_group():
    repository = make_repository()

    result = repository.search(SearchCriteria(surname="петров", group="ПИ-21"))

    assert len(result) == 3


def test_repository_search_by_surname_and_range():
    repository = make_repository()

    result = repository.search(SearchCriteria(surname="сидоров", min_total=25, max_total=35))

    assert len(result) == 1
    assert result[0].surname == "Сидоров"


def test_repository_search_by_group_and_range():
    repository = make_repository()

    result = repository.search(SearchCriteria(group="ПИ-21", min_total=25, max_total=35))

    assert len(result) == 1
    assert result[0].surname == "Сидоров"


def test_repository_search_by_surname_or_group_and_range():
    repository = make_repository()

    result = repository.search(SearchCriteria(surname="петров", group="ПИ-21", min_total=15, max_total=25))

    assert len(result) == 1
    assert result[0].surname == "Петров"


def test_repository_search_only_by_range():
    repository = make_repository()

    result = repository.search(SearchCriteria(min_total=15, max_total=25))

    assert len(result) == 1
    assert result[0].surname == "Петров"


def test_repository_search_without_criteria_returns_all():
    repository = make_repository()

    result = repository.search(SearchCriteria())

    assert len(result) == 3


def test_repository_delete_by_surname():
    repository = make_repository()

    deleted = repository.delete(DeleteCriteria(surname="иванов"))

    assert deleted == 1
    assert len(repository.get_all()) == 2


def test_repository_delete_by_group():
    repository = make_repository()

    deleted = repository.delete(DeleteCriteria(group="ПИ-21"))

    assert deleted == 2
    assert len(repository.get_all()) == 1


def test_repository_delete_by_range():
    repository = make_repository()

    deleted = repository.delete(DeleteCriteria(min_total=25, max_total=35))

    assert deleted == 1
    assert len(repository.get_all()) == 2