import tempfile
from pathlib import Path
from unittest.mock import patch

from src.cli.menu import CliMenu
from src.storage.json_repo import JsonRepository


def test_teacher_panel_exit():

    with tempfile.TemporaryDirectory() as tmp:

        repo = JsonRepository(Path(tmp) / "storage.json")
        menu = CliMenu(repo)

        inputs = [
            "5",
            "teacher123",

            "1",
            "t1",
            "math",
            "1",
            "q1",
            "2+2",
            "2",
            "3",
            "4",
            "2",

            "2",
            "invalid",

            "3",
            "invalid",
            "new title",

            "4",

            "0"
        ]

        with patch("builtins.input", side_effect=inputs):
            menu.run()