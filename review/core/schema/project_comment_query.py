import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from core.interactors.project_comment import get_all_project_comments, get_project_comment
from core.schema.enums import Evaluation
from ..models import ProjectComment


class ProjectCommentNode(DjangoObjectType):
    class Meta:
        model = ProjectComment
        fields = [
            'text',
        ]
        interfaces = (relay.Node,)

    rating = Evaluation()

    @classmethod
    def get_node(cls, info, id):
        return get_project_comment(info.context.user, id)


class ProjectCommentQuery(graphene.ObjectType):
    project_comment = relay.Node.Field(ProjectCommentNode)
    project_comments = graphene.List(graphene.NonNull(ProjectCommentNode), required=True)

    def resolve_project_comments(self, info):
        return get_all_project_comments(info.context.user)
