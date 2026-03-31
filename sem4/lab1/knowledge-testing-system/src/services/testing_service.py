from uuid import uuid4

from src.domain.enums import AttemptState
from src.domain.models import Attempt


class TestingService:

    def __init__(self, repo):
        self.repo = repo

    def start_attempt(self, student_id: str, test_id: str):
        attempt = Attempt(id=str(uuid4()), student_id=student_id, test_id=test_id)
        attempt.state = AttemptState.IN_PROGRESS
        self.repo.add_attempt(attempt)
        return attempt

    def answer(self, attempt_id: str, question_id: str, option_index: int):
        attempt = self.repo.get_attempt(attempt_id)
        attempt.answers[question_id] = option_index
        self.repo.update_attempt(attempt)

    def submit(self, attempt_id: str):
        attempt = self.repo.get_attempt(attempt_id)
        attempt.state = AttemptState.SUBMITTED
        self.repo.update_attempt(attempt)
