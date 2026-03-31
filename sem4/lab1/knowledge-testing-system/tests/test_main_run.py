from unittest.mock import patch
from src.main import main


def test_main_runs():

    with patch("builtins.input", side_effect=["0"]):
        main()