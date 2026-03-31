from pathlib import Path
import tempfile

from src.services.grading_service import GradingService
from src.storage.json_repo import JsonRepository
from src.domain.models import Test, Question, Attempt
from src.domain.enums import AttemptState


def test_grading_branches():

    with tempfile.TemporaryDirectory() as tmp:

        repo = JsonRepository(Path(tmp) / "storage.json")

        test = Test(
            id="t1",
            title="math",
            questions=[
                Question(
                    id="q1",
                    text="2+2",
                    options=["3", "4"],
                    correct_index=1
                )
            ]
        )

        repo.add_test(test)

        attempt = Attempt(
            id="a1",
            student_id="s1",
            test_id="t1",
            state=AttemptState.SUBMITTED,
            answers={"q1": 0},
            score=0
        )

        repo.add_attempt(attempt)

        grading = GradingService(repo)

        grade = grading.grade_attempt("a1")

        assert grade.value is not None