import json
import random
import pytest

from src.cube import RubiksCube

# ---------- фикстуры ----------
@pytest.fixture
def cube():
    return RubiksCube()  # собранный по умолчанию


@pytest.fixture
def solved_state_strs():
    # удобный словарь строк 9 символов на грань
    return {
        "U": "WWWWWWWWW",
        "D": "YYYYYYYYY",
        "L": "OOOOOOOOO",
        "R": "RRRRRRRRR",
        "F": "GGGGGGGGG",
        "B": "BBBBBBBBB",
    }


# ---------- базовые тесты ----------
def test_initial_is_solved(cube):
    assert cube.is_solved() is True


@pytest.mark.parametrize("face", list("UDLRFB"))
def test_four_turns_return_to_start(cube, face):
    before = cube.snapshot()
    for _ in range(4):
        cube.rotate(face, clockwise=True, turns=1)
    assert cube.snapshot() == before
    assert cube.is_solved() is True


@pytest.mark.parametrize("face", list("UDLRFB"))
def test_turn_and_inverse_restore(cube, face):
    before = cube.snapshot()
    cube.rotate(face, True, 1)
    cube.rotate(face, False, 1)
    assert cube.snapshot() == before
    assert cube.is_solved() is True


@pytest.mark.parametrize("face", list("UDLRFB"))
def test_double_equals_two_singles(cube, face):
    c1 = RubiksCube()
    c2 = RubiksCube()
    c1.rotate(face, True, 2)
    c2.rotate(face, True, 1)
    c2.rotate(face, True, 1)
    assert c1.snapshot() == c2.snapshot()


def test_is_solved_false_after_move(cube):
    cube.rotate("U", True, 1)
    assert cube.is_solved() is False


def test_reset_solved_restores(cube):
    cube.rotate("R", False, 1)
    assert cube.is_solved() is False
    cube.reset_solved()
    assert cube.is_solved() is True


def test_str_contains_all_faces(cube):
    s = str(cube)
    for f in "UDLRFB":
        assert f + "=" in s


# ---------- randomize ----------
def test_randomize_changes_state_deterministic():
    # фиксируем seed, чтобы тест был детерминированным
    random.seed(12345)
    c = RubiksCube()
    before = c.snapshot()
    c.randomize(10)
    after = c.snapshot()
    assert after != before
    assert c.is_solved() is False


# ---------- загрузка/сохранение ----------
def test_save_and_load_roundtrip(tmp_path):
    c1 = RubiksCube()
    c1.randomize(7)
    path = tmp_path / "state.json"
    c1.save_to_file(str(path))

    c2 = RubiksCube()
    c2.load_from_file(str(path))
    assert c2.snapshot() == c1.snapshot()


def test_load_invalid_length_raises(tmp_path, solved_state_strs):
    bad = solved_state_strs.copy()
    bad["U"] = "W" * 8  # меньше 9
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    c = RubiksCube()
    with pytest.raises(ValueError):
        c.load_from_file(str(p))


def test_load_invalid_missing_face_raises(tmp_path, solved_state_strs):
    bad = solved_state_strs.copy()
    del bad["B"]  # нет одной грани
    p = tmp_path / "bad2.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    c = RubiksCube()
    # Метод ожидает строку длиной 9; отсутствие ключа приведёт к None -> ValueError
    with pytest.raises(ValueError):
        c.load_from_file(str(p))


# ---------- ошибки ввода ----------
def test_invalid_face_raises(cube):
    with pytest.raises(ValueError):
        cube.rotate("X", True, 1)


def test_turns_normalization(cube):
    # turns % 4 -> 0 ничего не меняет (4*90° = полный оборот)
    before = cube.snapshot()
    cube.rotate("U", True, 4)
    assert cube.snapshot() == before
