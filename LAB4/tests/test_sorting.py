
import array
from src.sorting.CocktailSort import CocktailSort
from src.sorting.StrandSort import StrandSort
from src.sorting.Person import Person

def test_cocktail_sort_inplace_int():
    a = [5,3,4,1,2]
    CocktailSort.sort_inplace(a)
    assert a == [1,2,3,4,5]

def test_cocktail_sort_key_reverse():
    a = ["bbb","a","cc"]
    CocktailSort.sort_inplace(a, key=len, reverse=True)
    assert a == ["bbb","cc","a"]

def test_cocktail_sort_array_array():
    a = array.array('i', [3,1,2])
    # need to convert to list for in-place; but pure version returns list
    out = CocktailSort.sort(a)
    assert out == [1,2,3]

def test_strand_sort_returns_new_list():
    a = [4,2,5,1,3]
    out = StrandSort.sort(a)
    assert out == [1,2,3,4,5]
    assert a == [4,2,5,1,3]  # original unchanged

def test_strand_sort_inplace_custom_objects():
    people = [Person("Vlad", 18), Person("Anna", 21), Person("Oleg", 18), Person("Mia", 19)]
    StrandSort.sort_inplace(people, key=lambda p: (p.age, p.name))
    assert [repr(p) for p in people] == ["Oleg(18)", "Vlad(18)", "Mia(19)", "Anna(21)"]
