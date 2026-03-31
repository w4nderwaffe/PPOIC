import tempfile
from pathlib import Path

from src.storage.json_repo import JsonRepository
from src.domain.models import Question, Test


def test_repository_save_and_load_test():

    with tempfile.TemporaryDirectory() as tmp:

        path = Path(tmp) / "storage.json"

        repo = JsonRepository(path)

        test = Test(
            id="t1",
            title="python",
            questions=[
                Question(id="q1", text="what", options=["a", "b"], correct_index=0)
            ],
        )

        repo.add_test(test)

        tests = repo.list_tests()

        assert len(tests) == 1
        assert tests[0].id == "t1"