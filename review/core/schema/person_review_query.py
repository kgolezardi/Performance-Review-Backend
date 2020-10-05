import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.models import User
from accounts.schema.user_query import UserNode
from core.interactors.person_review import get_or_create_person_review, get_all_person_reviews, get_person_review, \
    get_user_person_reviews
from core.schema.enums import Evaluation, State, Phase
from graphql_api.schema.extension import Extension
from graphql_api.schema.utils import get_node
from .base_review import BaseReview
from ..interactors.settings import is_at_phase
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
        ]
        interfaces = (relay.Node, BaseReview,)

    sahabiness_rating = Evaluation()
    problem_solving_rating = Evaluation()
    execution_rating = Evaluation()
    thought_leadership_rating = Evaluation()
    leadership_rating = Evaluation()
    presence_rating = Evaluation()
    state = graphene.Field(State, required=True)

    reviewer = graphene.Field(UserNode)
    is_self_review = graphene.NonNull(graphene.Boolean)

    def resolve_reviewer(self, info):
        if not is_at_phase(Phase.MANAGER_REVIEW):
            return None
        user = info.context.user
        if not user == self.reviewee.manager:
            return None
        return self.reviewer

    def resolve_is_self_review(self, info):
        return self.is_self_review()

    @classmethod
    def get_node(cls, info, id):
        return get_person_review(info.context.user, id)


class UserNodePersonReviewExtension(Extension):
    class Meta:
        base = UserNode

    person_review = graphene.Field(PersonReviewNode,
                                   description="get or create a person review about this user from logged in user")
    person_reviews = graphene.List(graphene.NonNull(PersonReviewNode), required=True,
                                   description="list of person reviews about this user")

    def resolve_person_review(self, info):
        reviewer = info.context.user
        return get_or_create_person_review(reviewee=self, reviewer=reviewer)

    def resolve_person_reviews(self, info):
        user = info.context.user
        return get_user_person_reviews(user, reviewee=self)


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
