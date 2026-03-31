from src.sorting.CocktailSort import CocktailSort
from src.sorting.StrandSort import StrandSort
from src.sorting.Person import Person


def test_cocktail_sort_simple_ints():
    sorter = CocktailSort()
    data = [5, 1, 4, 2, 3]
    result = sorter.sort(data)
    assert result == [1, 2, 3, 4, 5]
    # исходный список не меняется
    assert data == [5, 1, 4, 2, 3]


def test_cocktail_sort_inplace_mutates():
    sorter = CocktailSort()
    data = [9, 0, -1, 3]
    sorter.sort_inplace(data)
    assert data == [-1, 0, 3, 9]


def test_cocktail_sort_reverse():
    sorter = CocktailSort(reverse=True)
    data = [1, 2, 3, 4]
    sorter.sort_inplace(data)
    assert data == [4, 3, 2, 1]


def test_cocktail_sort_with_key():
    # сортируем по длине строки
    sorter = CocktailSort(key=len)
    data = ["bbb", "a", "cccc", "dd"]
    result = sorter.sort(data)
    assert result == ["a", "dd", "bbb", "cccc"]


def test_strand_sort_simple_ints():
    sorter = StrandSort()
    data = [5, 1, 4, 2, 3]
    result = sorter.sort(data)
    assert result == [1, 2, 3, 4, 5]
    # исходный список не меняется
    assert data == [5, 1, 4, 2, 3]


def test_strand_sort_inplace_mutates():
    sorter = StrandSort()
    data = [10, -1, 7, 0]
    sorter.sort_inplace(data)
    assert data == [-1, 0, 7, 10]


def test_strand_sort_reverse():
    sorter = StrandSort(reverse=True)
    data = [1, 2, 3, 4]
    result = sorter.sort(data)
    assert result == [4, 3, 2, 1]


def test_strand_sort_with_key():
    sorter = StrandSort(key=len)
    data = ["bbb", "a", "cccc", "dd"]
    result = sorter.sort(data)
    assert result == ["a", "dd", "bbb", "cccc"]


def test_sort_person_by_age_then_name_cocktail():
    people = [
        Person("Vlad", 18),
        Person("Anna", 21),
        Person("Oleg", 18),
        Person("Mia", 19),
    ]
    sorter = CocktailSort(key=lambda p: (p.age, p.name))
    result = sorter.sort(people)
    assert [repr(p) for p in result] == ["Oleg(18)", "Vlad(18)", "Mia(19)", "Anna(21)"]


def test_sort_person_by_age_then_name_strand():
    people = [
        Person("Vlad", 18),
        Person("Anna", 21),
        Person("Oleg", 18),
        Person("Mia", 19),
    ]
    sorter = StrandSort(key=lambda p: (p.age, p.name))
    result = sorter.sort(people)
    assert [repr(p) for p in result] == ["Oleg(18)", "Vlad(18)", "Mia(19)", "Anna(21)"]