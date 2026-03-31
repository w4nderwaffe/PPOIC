from models.paginator import Paginator


def test_paginator_total_items_and_pages():
    paginator = Paginator(list(range(25)), page_size=10, current_page=1)

    assert paginator.total_items == 25
    assert paginator.total_pages == 3


def test_paginator_total_pages_for_empty_items():
    paginator = Paginator([], page_size=10, current_page=1)

    assert paginator.total_items == 0
    assert paginator.total_pages == 1
    assert paginator.get_page_items() == []


def test_paginator_get_first_page_items():
    paginator = Paginator(list(range(25)), page_size=10, current_page=1)

    assert paginator.get_page_items() == list(range(10))


def test_paginator_get_last_page_items():
    paginator = Paginator(list(range(25)), page_size=10, current_page=3)

    assert paginator.get_page_items() == list(range(20, 25))


def test_paginator_next_previous_first_last_page():
    paginator = Paginator(list(range(25)), page_size=10, current_page=1)

    paginator.next_page()
    assert paginator.current_page == 2

    paginator.next_page()
    assert paginator.current_page == 3

    paginator.next_page()
    assert paginator.current_page == 3

    paginator.previous_page()
    assert paginator.current_page == 2

    paginator.first_page()
    assert paginator.current_page == 1

    paginator.last_page()
    assert paginator.current_page == 3


def test_paginator_set_page_size_recalculates_pages():
    paginator = Paginator(list(range(25)), page_size=10, current_page=3)

    paginator.set_page_size(20)

    assert paginator.page_size == 20
    assert paginator.total_pages == 2
    assert paginator.current_page == 2


def test_paginator_set_page_handles_bounds():
    paginator = Paginator(list(range(25)), page_size=10, current_page=1)

    paginator.set_page(0)
    assert paginator.current_page == 1

    paginator.set_page(100)
    assert paginator.current_page == 3

    paginator.set_page(2)
    assert paginator.current_page == 2


def test_paginator_page_size_minimum_is_one():
    paginator = Paginator(list(range(5)), page_size=0, current_page=1)

    assert paginator.page_size == 1