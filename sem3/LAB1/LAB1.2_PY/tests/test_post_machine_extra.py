import io
import sys
import builtins
import types
import pytest

from src.post_machine import PostMachine, main as pm_main


def capture_output(fn, *args, **kwargs):
    old = sys.stdout
    buf = io.StringIO()
    try:
        sys.stdout = buf
        fn(*args, **kwargs)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_print_tape_on_empty_tape_shows_brackets():
    pm = PostMachine(3)
    pm.set_tape("")
    out = capture_output(pm.print_tape)
    assert out.strip() == "[]"


def test_left_right_on_empty_tape_prints_empty():
    pm = PostMachine(4)
    pm.set_tape("")
    out1 = capture_output(pm.execute, "LEFT")
    out2 = capture_output(pm.execute, "RIGHT")
    assert out1.strip() == "[]"
    assert out2.strip() == "[]"


def test_execute_is_case_insensitive_and_strips_spaces():
    pm = PostMachine(1)
    pm.set_tape("0")
    out = capture_output(pm.execute, "   mark   ")
    assert "[1]" in out


def test_execute_print_returns_and_prints():
    pm = PostMachine(3)
    pm.set_tape("010")
    s = pm.execute("PRINT")
    assert s == "0[1]0"


def test_repr_contains_core_fields():
    pm = PostMachine(5)
    r = repr(pm)
    assert "PostMachine(" in r and "size=20" not in r


def test_main_wrapper_delegates_to_cli(monkeypatch):
    calls = {"args": None}

    def fake_cli(argv=None):
        calls["args"] = argv
        return 0

    fake_module = types.ModuleType("src.post_machine_main")
    fake_module.main = fake_cli
    monkeypatch.setitem(sys.modules, "src.post_machine_main", fake_module)

    assert pm_main(None) == 0
    assert calls["args"] is None
