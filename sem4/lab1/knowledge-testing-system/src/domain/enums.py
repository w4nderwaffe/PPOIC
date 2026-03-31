from enum import Enum


class AttemptState(str, Enum):
    DRAFT = "Draft"
    IN_PROGRESS = "InProgress"
    SUBMITTED = "Submitted"
    GRADED = "Graded"
    FEEDBACK_PROVIDED = "FeedbackProvided"
    ARCHIVED = "Archived"
