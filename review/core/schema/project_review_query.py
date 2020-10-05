import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.models import User
from accounts.schema.user_query import UserNode
from core.enums import Phase
from core.interactors.project_review import get_all_project_reviews, get_project_review, get_users_to_review, \
    get_user_project_reviews
from core.interactors.settings import is_at_phase
from core.schema.enums import Evaluation
from graphql_api.schema.extension import Extension
from graphql_api.schema.utils import get_node
from .base_review import BaseReview
from ..models import ProjectReview


class ProjectReviewNode(DjangoObjectType):
    class Meta:
        model = ProjectReview
        fields = [
            'reviewee',
            'project',
            'text',
        ]
        interfaces = (relay.Node, BaseReview,)

    rating = Evaluation()
    reviewers = graphene.List(graphene.NonNull(UserNode), required=True)

    def resolve_reviewers(self, info):
        if not is_at_phase(Phase.SELF_REVIEW):
            return ProjectReview.objects.none()
        return self.reviewers.all()

    @classmethod
    def get_node(cls, info, id):
        return get_project_review(info.context.user, id)


class UserNodeProjectReviewExtension(Extension):
    class Meta:
        base = UserNode

    project_reviews = graphene.List(graphene.NonNull(ProjectReviewNode), required=True,
                                    description="list of project reviews about this user")

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
