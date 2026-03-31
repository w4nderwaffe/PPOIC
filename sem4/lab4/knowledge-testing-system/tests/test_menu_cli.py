import tempfile
from pathlib import Path
from unittest.mock import patch

from src.cli.menu import CliMenu
from src.storage.json_repo import JsonRepository


def test_menu_invalid_option():

    with tempfile.TemporaryDirectory() as tmp:

        repo = JsonRepository(Path(tmp) / "storage.json")
        menu = CliMenu(repo)

        inputs = [
            "9",
            "1",
            "2",
            "s1",
            "invalid",
            "3",
            "invalid",
            "4",
            "wrongpassword",
            "0"
        ]

        with patch("builtins.input", side_effect=inputs):
            menu.run()