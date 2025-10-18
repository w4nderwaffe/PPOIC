import json
import pytest
from src.cube import RubiksCube

def test_load_allows_nonstandard_symbols(tmp_path):
    # Текущая реализация НЕ валидирует алфавит стикеров — загрузка должна пройти без исключения
    data = {
        "U": "WWWWWWWWW",
        "D": "YYYYYYYYY",
        "L": "OOOOOOOOO",
        "R": "RRRRRRRRR",
        "F": "XXXXXXXXX",  # «левые» символы — допускаются текущей реализацией
        "B": "BBBBBBBBB",
    }
    p = tmp_path / "nonstandard.json"
    p.write_text(json.dumps(data), encoding="utf-8")

    c = RubiksCube()
    c.load_from_file(str(p))
    # Проверим, что загрузилось именно то, что записали (особенно F)
    assert "".join(c.faces["F"][r][c_] for r in range(3) for c_ in range(3)) == "XXXXXXXXX"

def test_load_raises_when_face_value_is_not_string(tmp_path):
    # Покрываем ветку с ValueError: если значение не строка длиной 9
    data = {
        "U": "WWWWWWWWW",
        "D": "YYYYYYYYY",
        "L": "OOOOOOOOO",
        "R": "RRRRRRRRR",
        "F": ["G"] * 9,     # не строка → должно упасть
        "B": "BBBBBBBBB",
    }
    p = tmp_path / "bad_type.json"
    p.write_text(json.dumps(data), encoding="utf-8")

    c = RubiksCube()
    with pytest.raises(ValueError):
        c.load_from_file(str(p))
