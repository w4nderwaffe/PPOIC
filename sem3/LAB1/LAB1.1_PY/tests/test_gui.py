import json
import types
import pytest
import sys
from pathlib import Path

# --- bootstrap путей: сначала КОРЕНЬ (чтоб импортировался пакет src),
# потом сам каталог src (чтоб внутри src/gui.py сработало "from cube import RubiksCube")
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))
# ---------------------------------------------------------------------

import src.gui as gui  # сам модуль
# NB: внутри gui имеется "from cube import RubiksCube" — благодаря sys.path выше это отработает.

@pytest.fixture
def app():
    """Создаём/скрываем Tk-приложение, корректно уничтожаем после теста."""
    a = gui.App()
    # прячем окно, чтоб не мигало в консоли/CI
    a.withdraw()
    yield a
    try:
        a.destroy()
    except Exception:
        pass


def test_menu_to_game_start_solved(app):
    # Меню -> игра (собранное состояние)
    app.start_solved()
    assert isinstance(app.game_frame, gui.GameFrame)
    assert app.game_frame.cube.is_solved() is True

    # Проверим отрисовку: на канвасе должны быть прямоугольники
    items = app.game_frame.canvas.find_all()
    assert len(items) >= 54  # 6 граней * 9 стикеров


def test_game_turn_and_double_then_reset(app):
    app.start_solved()
    gf = app.game_frame

    before = gf.cube.snapshot()
    gf.turn('U', True, 1)
    assert gf.cube.is_solved() is False
    # двойной прошлый ход (U2)
    gf.double_last_move()
    # После U + U2 состояние явно не равно исходному
    assert gf.cube.snapshot() != before

    # Сброс
    gf.reset()
    assert gf.cube.is_solved() is True
    # лейбл тоже обновился
    assert "Собран" in gf.solved_var.get() or "Solved" in gf.solved_var.get()


def test_scramble_and_redraw(app):
    app.start_solved()
    gf = app.game_frame
    gf.scramble(5)
    assert gf.cube.is_solved() is False
    # Перерисовка не падает
    gf.redraw()
    assert len(gf.canvas.find_all()) >= 54


def test_save_and_load_via_gui(tmp_path, monkeypatch, app):
    app.start_solved()
    gf = app.game_frame

    # Подменим пути сохранения на временные
    tmp_save_dir = tmp_path / "save_dir"
    tmp_save_path = tmp_save_dir / "cube_state.json"
    monkeypatch.setattr(gui, "SAVE_DIR", str(tmp_save_dir))
    monkeypatch.setattr(gui, "SAVE_PATH", str(tmp_save_path))

    # Подменим messagebox, чтобы не всплывали окна
    calls = {"info": [], "error": []}
    monkeypatch.setattr(gui.messagebox, "showinfo", lambda *a, **k: calls["info"].append((a, k)))
    monkeypatch.setattr(gui.messagebox, "showerror", lambda *a, **k: calls["error"].append((a, k)))

    # Сохраняем собранное состояние
    saved_before = gf.cube.snapshot()
    gf.save_to_fixed_path()
    assert tmp_save_path.exists()
    assert calls["info"]  # был вызов showinfo

    # Перемешаем и проверим, что состояние изменилось
    gf.scramble(3)
    assert gf.cube.snapshot() != saved_before

    # Мокаем диалог выбора файла, чтобы вернуть наш путь
    monkeypatch.setattr(gui.filedialog, "askopenfilename", lambda **_: str(tmp_save_path))

    # Загружаем — должно вернуть прежнее состояние
    gf.load_from_file_dialog()
    assert gf.cube.snapshot() == saved_before
    assert not calls["error"]


def test_app_start_from_file(tmp_path, monkeypatch, app):
    # Подготовим валидный JSON состояния (собранный)
    data = {
        "U": "WWWWWWWWW",
        "D": "YYYYYYYYY",
        "L": "OOOOOOOOO",
        "R": "RRRRRRRRR",
        "F": "GGGGGGGGG",
        "B": "BBBBBBBBB",
    }
    p = tmp_path / "state.json"
    p.write_text(json.dumps(data), encoding="utf-8")

    # Мокаем диалог, чтобы вернуть наш файл
    monkeypatch.setattr(gui.filedialog, "askopenfilename", lambda **_: str(p))
    # Мокаем messagebox на случай ошибок
    monkeypatch.setattr(gui.messagebox, "showerror", lambda *a, **k: (_ for _ in ()).throw(AssertionError("showerror called")))

    app.start_from_file()
    assert isinstance(app.game_frame, gui.GameFrame)
    assert app.game_frame.cube.is_solved() is True


def test_show_menu_and_back_to_game(app):
    app.start_solved()
    # Вернуться в меню
    app.show_menu()
    assert app.game_frame is None  # игра убрана
    # Снова игра
    app.start_random()
    assert isinstance(app.game_frame, gui.GameFrame)
