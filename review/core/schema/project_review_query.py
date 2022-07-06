import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.models import User
from accounts.schema.user_query import UserNode
from core.interactors.project_review import get_all_project_reviews, get_project_review, get_users_to_review, \
    get_user_project_reviews, get_project_review_reviewers, get_project_review_rating, get_project_review_answers
from core.schema.enums import Evaluation
from graphql_api.schema.extension import Extension
from graphql_api.schema.utils import get_node
from .answer_types import AnswerOutput
from ..models import ProjectReview


class ProjectReviewNode(DjangoObjectType):
    class Meta:
        model = ProjectReview
        fields = [
            'reviewee',
            'project_name',
            'consulted_with_manager',
            'approved_by_manager',
        ]
        interfaces = (relay.Node,)

    rating = Evaluation()
    answers = graphene.List(graphene.NonNull(AnswerOutput), required=True)
    reviewers = graphene.List(graphene.NonNull(UserNode), required=True)

    def resolve_rating(self, info):
        return get_project_review_rating(self)

    def resolve_answers(self, info):
        return get_project_review_answers(self)

    def resolve_reviewers(self, info):
        return get_project_review_reviewers(self)

    @classmethod
    def get_node(cls, info, id):
        return get_project_review(info.context.user, id)


class UserNodeProjectReviewExtension(Extension):
    class Meta:
        base = UserNode

    project_reviews = graphene.List(graphene.NonNull(ProjectReviewNode), required=True,
                                    description="List of project reviews about this user")

    def resolve_project_reviews(self, info):
        user = info.context.user
        return get_user_project_reviews(user, reviewee=self)


class ProjectReviewQuery(graphene.ObjectType):
    project_review = relay.Node.Field(ProjectReviewNode)
    project_reviews = graphene.List(graphene.NonNull(ProjectReviewNode), reviewee_id=graphene.ID(), required=True)

    users_to_review = graphene.List(graphene.NonNull(UserNode), required=True)

    def resolve_project_reviews(self, info, reviewee_id=None):
        user = info.context.user
        if reviewee_id is None:
            return get_all_project_reviews(user=user)
        reviewee = get_node(reviewee_id, info, User)
        return get_user_project_reviews(user=user, reviewee=reviewee)

    def resolve_users_to_review(self, info):
        return get_users_to_review(info.context.user)
