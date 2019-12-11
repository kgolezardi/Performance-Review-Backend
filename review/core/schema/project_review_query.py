import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.schema.user_query import UserNode
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
