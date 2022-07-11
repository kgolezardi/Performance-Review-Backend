from accounts.models import User
from core.models import Question
from graphql_api.schema.utils import get_node


def convert_ids_to_reviewers(reviewers_id, info):
    if reviewers_id is None:
        return None
    reviewers = [get_node(reviewer_id, info, User) for reviewer_id in reviewers_id]
    reviewers = list(filter(None, reviewers))  # remove None values
    return reviewers


def convert_answers_input(answers_input, info):
    if answers_input is None:
        return None
    return [(get_node(answer.question_id, info, Question), answer.value) for answer in answers_input]
