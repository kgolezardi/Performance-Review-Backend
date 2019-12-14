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

    @classmethod
    def base_query_set(cls, info):
        # TODO move this logic to interactor
        if info.context.user.is_authenticated:
            user=info.context.user
            return ProjectReview.objects.filter(reviewee=user)
        return ProjectReview.objects.none()

    @classmethod
    def get_node(cls, info, id):
        try:
            return ProjectReviewNode.base_query_set(info).get(id=id)
        except cls._meta.model.DoesNotExist:
            return None


class ProjectReviewQuery(graphene.ObjectType):
    project_review = relay.Node.Field(ProjectReviewNode)
    project_reviews = graphene.List(graphene.NonNull(ProjectReviewNode), required=True)

    def resolve_project_reviews(self, info):
        return ProjectReviewNode.base_query_set(info)
