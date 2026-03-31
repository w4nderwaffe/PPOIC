from unittest.mock import patch

import src.main


def test_main_runs():

    with patch("builtins.input", side_effect=["0"]):
        src.main.main()