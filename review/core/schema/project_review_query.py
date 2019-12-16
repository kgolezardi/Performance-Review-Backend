import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.schema.user_query import UserNode
from core.interactors.project_review import get_all_project_reviews, get_project_review
from core.schema.enums import Evaluation
from ..models import ProjectReview


class ProjectReviewNode(DjangoObjectType):
    class Meta:
        model = ProjectReview
        fields = [
            'project',
            'text',
        ]
        interfaces = (relay.Node,)

    rating = Evaluation()
    reviewers = graphene.List(graphene.NonNull(UserNode), required=True)

    def resolve_reviewers(self, info):
        return self.reviewers.all()

    @classmethod
    def get_node(cls, info, id):
        return get_project_review(info.context.user, id)


class ProjectReviewQuery(graphene.ObjectType):
    project_review = relay.Node.Field(ProjectReviewNode)
    project_reviews = graphene.List(graphene.NonNull(ProjectReviewNode), required=True)

    def resolve_project_reviews(self, info):
        return get_all_project_reviews(info.context.user)
