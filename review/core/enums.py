from utils.base_enum import BaseEnum


class Evaluation(BaseEnum):
    NEEDS_IMPROVEMENT = 1
    MEETS_EXPECTATIONS = 2
    EXCEEDS_EXPECTATIONS = 3
    STRONGLY_EXCEEDS_EXPECTATIONS = 4
    SUPERB = 5


class Phase(BaseEnum):
    SELF_REVIEW = 1
    PEER_REVIEW = 2
    MANAGER_REVIEW = 3
    RESULTS = 4
