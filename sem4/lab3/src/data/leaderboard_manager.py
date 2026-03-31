import json
from pathlib import Path


class LeaderboardManager:
    def __init__(self, path="config/leaderboard.json", limit=10):
        self.path = Path(path)
        self.limit = limit
        self.records = []
        self._ensure_file()
        self.load()

    def _ensure_file(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def load(self):
        try:
            content = self.path.read_text(encoding="utf-8").strip()
            self.records = json.loads(content) if content else []
        except (json.JSONDecodeError, OSError):
            self.records = []

        self.records.sort(key=lambda record: record.get("score", 0), reverse=True)
        self.records = self.records[:self.limit]

    def save(self):
        self.path.write_text(json.dumps(self.records, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_records(self):
        return list(self.records)

    def get_first_score(self):
        if not self.records:
            return None
        return self.records[0].get("score", 0)

    def is_first_place(self, score):
        first_score = self.get_first_score()
        if first_score is None:
            return True
        return score > first_score

    def add_record(self, name, score):
        clean_name = name.strip()
        if not clean_name:
            clean_name = "PLAYER"

        self.records.append({
            "name": clean_name[:12],
            "score": int(score)
        })
        self.records.sort(key=lambda record: record.get("score", 0), reverse=True)
        self.records = self.records[:self.limit]
        self.save()