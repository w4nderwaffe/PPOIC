# -*- coding: utf-8 -*-
import io
import sys
import pytest

from src.post_machine import PostMachine


def capture_output(func, *args, **kwargs):
    old = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_execute_strips_whitespace_commands():
    pm = PostMachine(3)
    pm.set_tape("010")     # head = 1
    out = capture_output(pm.execute, "   RIGHT   ")
    assert pm.head == 2
    assert "[0]" in out  # печать ленты после валидной команды


def test_mark_erase_on_initially_empty_tape_path():
    pm = PostMachine(5)
    pm.set_tape("")  # пустая лента
    # MARK должен создать [1] и распечатать
    out = capture_output(pm.execute, "MARK")
    assert pm.tape == [1]
    assert pm.head == 0
    assert "[1]" in out
    # ERASE должен поставить 0
    out = capture_output(pm.execute, "ERASE")
    assert pm.tape == [0]
    assert "[0]" in out


def test_multiple_boundary_moves_left_right_do_not_crash():
    pm = PostMachine(2)  # head = 1
    # упираемся вправо и двигаемся
    capture_output(pm.execute, "RIGHT")  # остаёмся на 1
    assert pm.head == 1
    # уходим влево до 0
    capture_output(pm.execute, "LEFT")
    assert pm.head == 0
    # за левую границу: не двигается
    for _ in range(3):
        capture_output(pm.execute, "LEFT")
    assert pm.head == 0
