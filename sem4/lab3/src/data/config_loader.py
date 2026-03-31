import json
from pathlib import Path


class ConfigLoader:
    @staticmethod
    def load_json(path):
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)