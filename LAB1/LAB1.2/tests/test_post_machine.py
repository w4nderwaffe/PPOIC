# -*- coding: utf-8 -*-
import io
import sys
import pytest

from src.post_machine import PostMachine


# --- вспомогательные утилиты ---
def capture_output(func, *args, **kwargs):
    """Перехватывает stdout при выполнении функции."""
    old = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = old
    return buf.getvalue()


# --- базовые тесты ---
def test_init_default_and_custom():
    pm = PostMachine()
    assert len(pm.tape) == 20
    assert pm.head == 10
    pm2 = PostMachine(7)
    assert len(pm2.tape) == 7
    assert pm2.head == 3


@pytest.mark.parametrize("bad_size", [0, -5])
def test_init_invalid_size_raises(bad_size):
    with pytest.raises(ValueError):
        PostMachine(bad_size)


# --- set_tape ---
def test_set_tape_filters_and_head_position():
    pm = PostMachine(5)
    pm.set_tape("00a101b")
    assert pm.tape == [0, 0, 1, 0, 1]
    assert pm.head == 2


def test_set_tape_empty_allows_and_next_commands_work():
    pm = PostMachine()
    pm.set_tape("")
    assert pm.tape == []
    assert pm.head == 0

    # MARK создаёт [1]
    out = capture_output(pm.execute, "MARK")
    assert pm.tape == [1]
    assert "[1]" in out

    # ERASE снова превращает в [0]
    out = capture_output(pm.execute, "ERASE")
    assert pm.tape == [0]
    assert "[0]" in out


# --- движение ---
def test_execute_left_and_right_with_boundaries():
    pm = PostMachine(4)
    # RIGHT: 2 -> 3
    capture_output(pm.execute, "RIGHT")
    assert pm.head == 3
    # RIGHT за границей — остаётся на месте
    capture_output(pm.execute, "RIGHT")
    assert pm.head == 3
    # LEFT: 3 -> 2 -> 1 -> 0
    for _ in range(3):
        capture_output(pm.execute, "LEFT")
    assert pm.head == 0
    # LEFT на границе не двигает
    capture_output(pm.execute, "LEFT")
    assert pm.head == 0


# --- изменение содержимого ---
def test_execute_mark_and_erase_toggle():
    pm = PostMachine(3)
    out = capture_output(pm.execute, "MARK")
    assert "[1]" in out and pm.tape[pm.head] == 1
    out = capture_output(pm.execute, "ERASE")
    assert "[0]" in out and pm.tape[pm.head] == 0


# --- неизвестная команда ---
def test_execute_unknown_command_prints_no_tape(capsys):
    pm = PostMachine(5)
    pm.set_tape("01010")
    pm.execute("SOMETHING")
    out = capsys.readouterr().out
    assert "Неизвестная команда" in out
    assert "[" not in out and "]" not in out


# --- STOP команда ---
def test_execute_stop_exits_and_prints_message(capsys):
    pm = PostMachine(5)
    with pytest.raises(SystemExit) as e:
        pm.execute("STOP")
    assert e.value.code == 0
    out = capsys.readouterr().out
    assert "Остановка машины." in out


# --- print_tape напрямую ---
def test_print_tape_format_includes_brackets():
    pm = PostMachine(5)
    pm.set_tape("10101")
    out = capture_output(pm.print_tape)
    assert out.count("[") == 1
    assert out.count("]") == 1
    assert any(x in out for x in ["[1]", "[0]"])


# --- edge-case: пустая лента и неизвестная команда ---
def test_execute_unknown_on_empty_tape(capsys):
    pm = PostMachine()
    pm.set_tape("")
    pm.execute("XYZ")
    out = capsys.readouterr().out
    assert "Неизвестная команда" in out


# --- edge-case: цепочка команд для комбинированного покрытия ---
def test_sequence_of_commands_combined_behavior():
    pm = PostMachine(6)
    pm.set_tape("000000")
    sequence = ["MARK", "RIGHT", "MARK", "LEFT", "ERASE", "LEFT", "ERASE"]
    for cmd in sequence:
        capture_output(pm.execute, cmd)
    # Проверим финальное состояние
    assert pm.tape.count(1) >= 1
    assert 0 <= pm.head < len(pm.tape)
