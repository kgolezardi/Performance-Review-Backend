import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from core.interactors.manager_project_comment import get_all_manager_project_comments, get_manager_project_comment, \
    get_or_create_manager_project_comment
from core.schema.enums import Evaluation
from graphql_api.schema.extension import Extension
from .base_project_comment import BaseProjectComment
from .project_review_query import ProjectReviewNode
from ..models import ManagerProjectComment


class ManagerProjectCommentNode(DjangoObjectType):
    class Meta:
        model = ManagerProjectComment
        fields = [
            'project_review',
        ]
        interfaces = (relay.Node, BaseProjectComment,)

    rating = Evaluation()

    @classmethod
    def get_node(cls, info, id):
        return get_manager_project_comment(info.context.user, id)


class ProjectReviewNodeManagerCommentsExtension(Extension):
    class Meta:
        base = ProjectReviewNode

    manager_comment = graphene.Field(ManagerProjectCommentNode,
                                     description="get or create a manager project comment about this project review "
                                                 "from the logged in user")

    def resolve_manager_comment(self, info):
        manager = info.context.user
        return get_or_create_manager_project_comment(project_review=self, manager=manager)


class ManagerProjectCommentQuery(graphene.ObjectType):
    manager_project_comment = relay.Node.Field(ManagerProjectCommentNode)
    manager_project_comments = graphene.List(graphene.NonNull(ManagerProjectCommentNode), required=True)

    def resolve_manager_project_comments(self, info):
        return get_all_manager_project_comments(info.context.user)
