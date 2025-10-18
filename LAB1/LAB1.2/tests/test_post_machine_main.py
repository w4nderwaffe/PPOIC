# -*- coding: utf-8 -*-
import builtins
import io
import sys
import pytest

from src.post_machine import main


def run_with_inputs(lines):
    """
    Запускает main(), подменяя input() на заданные строки.
    Возвращает stdout.
    """
    it = iter(lines)
    def fake_input(prompt=""):
        # эмулируем input() с подсказкой
        return next(it)

    old_inp = builtins.input
    old_stdout = sys.stdout
    buf = io.StringIO()
    try:
        builtins.input = fake_input
        sys.stdout = buf
        with pytest.raises(SystemExit) as e:
            main()
        # Ожидаем, что STOP завершит программу с кодом 0
        assert e.value.code == 0
    finally:
        builtins.input = old_inp
        sys.stdout = old_stdout
    return buf.getvalue()


def test_main_happy_path_with_commands_and_stop():
    # 1) ввод начального состояния
    # 2) несколько команд + STOP
    out = run_with_inputs([
        "00101",   # начальная лента
        "MARK",    # пометить текущую ячейку
        "RIGHT",   # сдвиг
        "ERASE",   # стереть
        "SOMETHING",  # неизвестная команда
        "STOP",    # остановка
    ])
    # Проверим ключевые сообщения и факты
    assert "Введите начальное состояние ленты" in out
    assert "Машина Поста готова" in out
    assert "Неизвестная команда: SOMETHING" in out
    # после каждой валидной команды должна быть отрисована лента со скобками
    # (минимум один раз убедимся)
    assert "[" in out and "]" in out


def test_main_empty_command_is_ignored_then_stop():
    # пустая строка команды игнорируется циклом (continue), затем STOP
    out = run_with_inputs([
        "101",  # состояние
        "",     # пустая команда -> игнор
        "STOP",
    ])
    assert "Введите начальное состояние" in out
    assert "Машина Поста готова" in out
