import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.models import User
from accounts.schema.user_query import UserNode
from core.interactors.person_review import get_or_create_person_review, get_all_person_reviews, get_person_review, \
    get_user_person_reviews, get_person_review_reviewer, get_or_create_self_person_review, \
    get_or_create_peer_person_review
from core.schema.enums import Evaluation, State
from graphql_api.schema.extension import Extension
from graphql_api.schema.utils import get_node
from ..models import PersonReview


class PersonReviewNode(DjangoObjectType):
    class Meta:
        model = PersonReview
        fields = [
            'reviewee',
            'strengths',
            'weaknesses',
        ]
        interfaces = (relay.Node,)

    state = graphene.Field(State, required=True)
    reviewer = graphene.Field(UserNode)
    is_self_review = graphene.NonNull(graphene.Boolean)

    def resolve_reviewer(self, info):
        user = info.context.user
        return get_person_review_reviewer(user, self)

    def resolve_is_self_review(self, info):
        return self.is_self_review()

    @classmethod
    def get_node(cls, info, id):
        return get_person_review(info.context.user, id)


class UserNodePersonReviewExtension(Extension):
    class Meta:
        base = UserNode

    self_person_review = graphene.Field(PersonReviewNode,
                                        description="Get (or create for self) a self person review about this user")
    peer_person_review = graphene.Field(PersonReviewNode,
                                        description="Get (or create for peer) a peer person review about this user")
    person_reviews = graphene.List(graphene.NonNull(PersonReviewNode), required=True,
                                   description="List of person reviews about this user")

    def resolve_self_person_review(self, info):
        user = info.context.user
        return get_or_create_self_person_review(reviewee=self, user=user)

    def resolve_peer_person_review(self, info):
        user = info.context.user
        return get_or_create_peer_person_review(reviewee=self, user=user)

    def resolve_person_reviews(self, info):
        user = info.context.user
        return get_user_person_reviews(user, reviewee=self)


class PersonReviewQuery(graphene.ObjectType):
    person_review = relay.Node.Field(PersonReviewNode)
    person_reviews = graphene.List(graphene.NonNull(PersonReviewNode), required=True)

    def resolve_person_reviews(self, info):
        return get_all_person_reviews(info.context.user)
