from utils.base_enum import BaseEnum


class Evaluation(BaseEnum):
    NEEDS_IMPROVEMENT = 1
    MEETS_EXPECTATIONS = 2
    EXCEEDS_EXPECTATIONS = 3
    SUPERB = 4


class Phase(BaseEnum):
    SELF_REVIEW = 1
    PEER_REVIEW = 2
    MANAGER_REVIEW = 3
    RESULTS = 4
    IDLE = 5
    MANAGER_ADJUSTMENT = 6


class State(BaseEnum):
    TODO = 1
    DOING = 2
    DONE = 3


class QuestionType(BaseEnum):
    TEXT = 1
    CHECKBOX_MULTIPLE = 2
