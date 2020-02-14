import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.models import User
from core.interactors.person_review import get_or_create_person_review, get_all_person_reviews, get_person_review
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
            'weaknesses',
            'final_submit',
        ]
        interfaces = (relay.Node,)

    sahabiness_rating = Evaluation()
    problem_solving_rating = Evaluation()
    execution_rating = Evaluation()
    thought_leadership_rating = Evaluation()
    leadership_rating = Evaluation()
    presence_rating = Evaluation()

    is_self_review = graphene.NonNull(graphene.Boolean)

    def resolve_is_self_review(self, info):
        return self.is_self_review()

    @classmethod
    def get_node(cls, info, id):
        return get_person_review(info.context.user, id)


class PersonReviewQuery(graphene.ObjectType):
    person_review = relay.Node.Field(PersonReviewNode)
    person_reviews = graphene.List(graphene.NonNull(PersonReviewNode), required=True)
    find_person_review = graphene.Field(PersonReviewNode, reviewee_id=graphene.ID())

    def resolve_person_reviews(self, info):
        return get_all_person_reviews(info.context.user)

    def resolve_find_person_review(self, info, reviewee_id):
        reviewee = get_node(reviewee_id, info, User)
        reviewer = info.context.user
        return get_or_create_person_review(reviewee=reviewee, reviewer=reviewer)
