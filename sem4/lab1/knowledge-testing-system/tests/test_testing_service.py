import tempfile
from pathlib import Path

from src.services.testing_service import TestingService
from src.storage.json_repo import JsonRepository
from src.domain.models import Question, Test


def test_start_attempt_and_submit():

    with tempfile.TemporaryDirectory() as tmp:

        repo = JsonRepository(Path(tmp) / "storage.json")

        test = Test(
            id="t1",
            title="math",
            questions=[
                Question(id="q1", text="2+2", options=["3", "4"], correct_index=1)
            ],
        )

        repo.add_test(test)

        service = TestingService(repo)

        attempt = service.start_attempt("s1", "t1")

        service.answer(attempt.id, "q1", 1)

        service.submit(attempt.id)

        saved = repo.get_attempt(attempt.id)

        assert saved.answers["q1"] == 1