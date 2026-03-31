from abc import ABC, abstractmethod
from typing import List

from src.domain.models import Attempt, Feedback, Grade, Student, Teacher, Test


class Repository(ABC):

    @abstractmethod
    def add_student(self, student: Student) -> None:
        pass

    @abstractmethod
    def add_teacher(self, teacher: Teacher) -> None:
        pass

    @abstractmethod
    def add_test(self, test: Test) -> None:
        pass

    @abstractmethod
    def list_tests(self) -> List[Test]:
        pass

    @abstractmethod
    def get_test(self, test_id: str) -> Test:
        pass

    @abstractmethod
    def add_attempt(self, attempt: Attempt) -> None:
        pass

    @abstractmethod
    def update_attempt(self, attempt: Attempt) -> None:
        pass

    @abstractmethod
    def get_attempt(self, attempt_id: str) -> Attempt:
        pass

    @abstractmethod
    def save_grade(self, grade: Grade) -> None:
        pass

    @abstractmethod
    def save_feedback(self, feedback: Feedback) -> None:
        pass
