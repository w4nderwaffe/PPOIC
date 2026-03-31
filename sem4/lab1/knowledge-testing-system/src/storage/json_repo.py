import json
from dataclasses import asdict
from pathlib import Path

from src.domain.models import Attempt, Feedback, Grade, Question, Student, Teacher, Test
from src.domain.enums import AttemptState


class JsonRepository:

    def __init__(self, path: Path):
        self.path = path
        self.data = {
            "students": {},
            "teachers": {},
            "tests": {},
            "attempts": {},
            "grades": {},
            "feedback": {}
        }

        if path.exists():
            self.data = json.loads(path.read_text())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            self._save()

    def _save(self):
        self.path.write_text(json.dumps(self.data, indent=2))

    def add_student(self, student: Student):
        self.data["students"][student.id] = asdict(student)
        self._save()

    def add_teacher(self, teacher: Teacher):
        self.data["teachers"][teacher.id] = asdict(teacher)
        self._save()

    def add_test(self, test: Test):
        payload = asdict(test)
        self.data["tests"][test.id] = payload
        self._save()

    def list_tests(self):
        tests = []
        for t in self.data["tests"].values():
            questions = [Question(**q) for q in t["questions"]]
            tests.append(Test(id=t["id"], title=t["title"], questions=questions))
        return tests

    def get_test(self, test_id: str):
        t = self.data["tests"][test_id]
        questions = [Question(**q) for q in t["questions"]]
        return Test(id=t["id"], title=t["title"], questions=questions)

    def add_attempt(self, attempt: Attempt):
        d = asdict(attempt)
        d["state"] = attempt.state.value
        self.data["attempts"][attempt.id] = d
        self._save()

    def update_attempt(self, attempt: Attempt):
        d = asdict(attempt)
        d["state"] = attempt.state.value
        self.data["attempts"][attempt.id] = d
        self._save()

    def get_attempt(self, attempt_id: str):
        a = self.data["attempts"][attempt_id]
        return Attempt(
            id=a["id"],
            student_id=a["student_id"],
            test_id=a["test_id"],
            state=AttemptState(a["state"]),
            answers=a["answers"],
            score=a["score"]
        )

    def save_grade(self, grade: Grade):
        self.data["grades"][grade.attempt_id] = asdict(grade)
        self._save()

    def save_feedback(self, feedback: Feedback):
        self.data["feedback"][feedback.attempt_id] = asdict(feedback)
        self._save()
