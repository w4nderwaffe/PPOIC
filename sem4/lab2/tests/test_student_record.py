import pytest

from models.student_record import StudentRecord


def test_student_record_creates_valid_object():
    record = StudentRecord(
        full_name="  Иванов Иван Иванович  ",
        group="  ПИ-21  ",
        social_work=["1", "2", "0", "3", "1", "4", "2", "0", "1", "2"]
    )

    assert record.full_name == "Иванов Иван Иванович"
    assert record.group == "ПИ-21"
    assert record.social_work == [1, 2, 0, 3, 1, 4, 2, 0, 1, 2]
    assert record.surname == "Иванов"
    assert record.total_social_work == 16


def test_student_record_raises_if_social_work_not_10_values():
    with pytest.raises(ValueError, match="10 значений"):
        StudentRecord(
            full_name="Иванов Иван Иванович",
            group="ПИ-21",
            social_work=[1, 2, 3]
        )


def test_student_record_raises_if_social_work_has_negative_value():
    with pytest.raises(ValueError, match="не могут быть отрицательными"):
        StudentRecord(
            full_name="Иванов Иван Иванович",
            group="ПИ-21",
            social_work=[1, 2, 3, 4, 5, -1, 0, 1, 2, 3]
        )


def test_student_record_raises_if_full_name_is_empty():
    with pytest.raises(ValueError, match="ФИО не может быть пустым"):
        StudentRecord(
            full_name="   ",
            group="ПИ-21",
            social_work=[0] * 10
        )


def test_student_record_raises_if_group_is_empty():
    with pytest.raises(ValueError, match="Группа не может быть пустой"):
        StudentRecord(
            full_name="Иванов Иван Иванович",
            group="   ",
            social_work=[0] * 10
        )


def test_student_record_surname_empty_when_name_empty_parts_impossible_but_property_safe():
    record = StudentRecord(
        full_name="Петров",
        group="ПИ-22",
        social_work=[0] * 10
    )

    assert record.surname == "Петров"