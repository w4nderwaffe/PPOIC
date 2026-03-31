from dataclasses import dataclass, field
from typing import Dict, List

from .enums import AttemptState


@dataclass
class Student:
    id: str
    name: str


@dataclass
class Teacher:
    id: str
    name: str


@dataclass
class Question:
    id: str
    text: str
    options: List[str]
    correct_index: int


@dataclass
class Test:
    id: str
    title: str
    questions: List[Question] = field(default_factory=list)


@dataclass
class Attempt:
    id: str
    student_id: str
    test_id: str
    state: AttemptState = AttemptState.DRAFT
    answers: Dict[str, int] = field(default_factory=dict)
    score: int = 0


@dataclass
class Grade:
    attempt_id: str
    value: str


@dataclass
class Feedback:
    attempt_id: str
    teacher_id: str
    message: str
