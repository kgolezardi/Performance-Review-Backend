from graphene import relay
from graphene_django import DjangoObjectType

from core.schema.enums import Evaluation
from ..models import PersonReview


class PersonReviewNode(DjangoObjectType):
    class Meta:
        model = PersonReview
        fields = [
            'reviewee',
            'sahabiness_comment',
            'problem_solving_comment',
            'execution_comment',
            'thought_leadership_comment',
            'leadership_comment',
            'presence_comment',
            'strengths',
            'weaknesses'
        ]
        interfaces = (relay.Node,)

    sahabiness_rating = Evaluation()
    problem_solving_rating = Evaluation()
    execution_rating = Evaluation()
    thought_leadership_rating = Evaluation()
    leadership_rating = Evaluation()
    presence_rating = Evaluation()
