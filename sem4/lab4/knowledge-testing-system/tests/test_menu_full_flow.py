import tempfile
from pathlib import Path
from unittest.mock import patch

from src.cli.menu import CliMenu
from src.storage.json_repo import JsonRepository


def test_menu_full_flow():

    with tempfile.TemporaryDirectory() as tmp:

        repo = JsonRepository(Path(tmp) / "storage.json")
        menu = CliMenu(repo)

        inputs = [
            "5",
            "teacher123",
            "1",
            "t1",
            "test",
            "1",
            "q1",
            "2+2",
            "2",
            "3",
            "4",
            "2",
            "4",

            "1",

            "2",
            "s1",
            "t1",
            "2",

            "3",
            "invalid",

            "4",
            "teacher123",
            "invalid",
            "t1",
            "ok",

            "0"
        ]

        with patch("builtins.input", side_effect=inputs):
            menu.run()