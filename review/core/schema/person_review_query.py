import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.models import User
from core.interactors import get_person_review
from core.schema.enums import Evaluation
from graphql_api.schema.utils import get_node
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


class PersonReviewQuery(graphene.ObjectType):
    person_review = graphene.Field(PersonReviewNode, reviewee_id=graphene.ID())

    def resolve_person_review(self, info, reviewee_id):
        reviewee = get_node(reviewee_id, info, User)
        reviewer = info.context.user
        return get_person_review(reviewee, reviewer)
