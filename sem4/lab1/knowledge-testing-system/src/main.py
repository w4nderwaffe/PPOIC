from pathlib import Path

from src.cli.menu import CliMenu
from src.storage.json_repo import JsonRepository


def main() -> None:
    repo = JsonRepository(Path("data/storage.json"))
    CliMenu(repo).run()


if __name__ == "__main__":
    main()
