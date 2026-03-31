import tempfile
from pathlib import Path

from src.storage.json_repo import JsonRepository
from src.domain.models import Feedback


def test_feedback_save():

    with tempfile.TemporaryDirectory() as tmp:

        repo = JsonRepository(Path(tmp) / "storage.json")

        feedback = Feedback(
            attempt_id="a1",
            teacher_id="t1",
            message="good"
        )

        repo.save_feedback(feedback)

        stored = repo.data["feedback"]["a1"]

        assert stored["message"] == "good"