import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.schema.user_query import UserNode
from core.interactors.manager_person_review import get_or_create_manager_person_review, get_all_manager_person_reviews, \
    get_manager_person_review
from core.schema.enums import Evaluation
from graphql_api.schema.extension import Extension
from ..models import ManagerPersonReview


class ManagerPersonReviewNode(DjangoObjectType):
    class Meta:
        model = ManagerPersonReview
        fields = [
            'reviewee',
            'strengths',
            'weaknesses',
        ]
        interfaces = (relay.Node,)

    overall_rating = Evaluation()

    @classmethod
    def get_node(cls, info, id):
        return get_manager_person_review(info.context.user, id)


class UserNodeManagerPersonReviewExtension(Extension):
    class Meta:
        base = UserNode

    manager_person_review = graphene.Field(ManagerPersonReviewNode,
                                           description="Get (or create for manager) a manager person review about this "
                                                       "user")

    def resolve_manager_person_review(self, info):
        user = info.context.user
        return get_or_create_manager_person_review(reviewee=self, user=user)


class ManagerPersonReviewQuery(graphene.ObjectType):
    manager_person_review = relay.Node.Field(ManagerPersonReviewNode)
    manager_person_reviews = graphene.List(graphene.NonNull(ManagerPersonReviewNode), required=True)

    def resolve_manager_person_reviews(self, info):
        return get_all_manager_person_reviews(info.context.user)
