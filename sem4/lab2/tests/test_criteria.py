from models.criteria import SearchCriteria, DeleteCriteria


def test_search_criteria_normalized_surname():
    criteria = SearchCriteria(surname="  ИВАНОВ  ")
    assert criteria.normalized_surname() == "иванов"


def test_search_criteria_normalized_surname_returns_none_for_empty():
    criteria = SearchCriteria(surname="   ")
    assert criteria.normalized_surname() is None


def test_search_criteria_normalized_surname_returns_none_for_none():
    criteria = SearchCriteria(surname=None)
    assert criteria.normalized_surname() is None


def test_delete_criteria_normalized_surname():
    criteria = DeleteCriteria(surname="  ПЕТРОВ ")
    assert criteria.normalized_surname() == "петров"


def test_delete_criteria_normalized_surname_returns_none_for_empty():
    criteria = DeleteCriteria(surname="   ")
    assert criteria.normalized_surname() is None