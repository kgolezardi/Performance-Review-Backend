from graphene import relay
from graphene_django import DjangoObjectType

from ..models import ProjectReview


class ProjectReviewNode(DjangoObjectType):
    class Meta:
        model = ProjectReview
        fields = [
            'project',
            'text',
            'rating',
            'reviewers'
        ]
        interfaces = (relay.Node,)
