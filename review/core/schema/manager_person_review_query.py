import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.models import User
from accounts.schema.user_query import UserNode
from core.interactors.manager_person_review import get_or_create_manager_person_review, get_all_manager_person_reviews, \
    get_manager_person_review
from core.schema.enums import Evaluation
from graphql_api.schema.extension import Extension
from graphql_api.schema.utils import get_node
from .base_review import BaseReview
from ..models import ManagerPersonReview


class ManagerPersonReviewNode(DjangoObjectType):
    class Meta:
        model = ManagerPersonReview
        fields = [
            'reviewee',
        ]
        interfaces = (relay.Node, BaseReview,)

    sahabiness_rating = Evaluation()
    problem_solving_rating = Evaluation()
    execution_rating = Evaluation()
    thought_leadership_rating = Evaluation()
    leadership_rating = Evaluation()
    presence_rating = Evaluation()
    overall_rating = Evaluation()

    @classmethod
    def get_node(cls, info, id):
        return get_manager_person_review(info.context.user, id)


class UserNodeManagerPersonReviewExtension(Extension):
    class Meta:
        base = UserNode

    manager_person_review = graphene.Field(ManagerPersonReviewNode,
                                           description="get or create a manager person review about this user from "
                                                       "logged in user")

    def resolve_manager_person_review(self, info):
        manager = info.context.user
        return get_or_create_manager_person_review(reviewee=self, manager=manager)


class ManagerPersonReviewQuery(graphene.ObjectType):
    manager_person_review = relay.Node.Field(ManagerPersonReviewNode)
    manager_person_reviews = graphene.List(graphene.NonNull(ManagerPersonReviewNode), required=True)
    find_manager_person_review = graphene.Field(ManagerPersonReviewNode, reviewee_id=graphene.ID())

    def resolve_manager_person_reviews(self, info):
        return get_all_manager_person_reviews(info.context.user)

    def resolve_find_manager_person_review(self, info, reviewee_id):
        reviewee = get_node(reviewee_id, info, User)
        manager = info.context.user
        return get_or_create_manager_person_review(reviewee=reviewee, manager=manager)
