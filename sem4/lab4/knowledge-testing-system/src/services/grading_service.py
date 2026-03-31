from src.domain.enums import AttemptState
from src.domain.models import Grade


class GradingService:

    def __init__(self, repo):
        self.repo = repo

    def grade_attempt(self, attempt_id: str):
        attempt = self.repo.get_attempt(attempt_id)
        test = self.repo.get_test(attempt.test_id)

        score = 0
        for q in test.questions:
            if attempt.answers.get(q.id) == q.correct_index:
                score += 1

        attempt.score = score
        attempt.state = AttemptState.GRADED
        self.repo.update_attempt(attempt)

        percent = score / len(test.questions) * 100

        if percent >= 90:
            value = "A"
        elif percent >= 75:
            value = "B"
        elif percent >= 60:
            value = "C"
        elif percent >= 45:
            value = "D"
        else:
            value = "F"

        grade = Grade(attempt_id=attempt.id, value=value)
        self.repo.save_grade(grade)

        return grade
