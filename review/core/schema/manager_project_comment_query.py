import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from core.interactors.manager_project_comment import get_all_manager_project_comments, get_manager_project_comment, \
    get_or_create_manager_project_comment, get_manager_project_comment_answers
from core.schema.enums import Evaluation
from graphql_api.schema.extension import Extension
from .answer_types import AnswerOutput
from .project_review_query import ProjectReviewNode
from ..models import ManagerProjectComment


class ManagerProjectCommentNode(DjangoObjectType):
    class Meta:
        model = ManagerProjectComment
        fields = [
            'project_review',
        ]
        interfaces = (relay.Node,)

    rating = Evaluation()
    answers = graphene.List(graphene.NonNull(AnswerOutput), required=True)

    @classmethod
    def get_node(cls, info, id):
        return get_manager_project_comment(info.context.user, id)

    def resolve_answers(self, info):
        return get_manager_project_comment_answers(self)


class ProjectReviewNodeManagerCommentsExtension(Extension):
    class Meta:
        base = ProjectReviewNode

    manager_comment = graphene.Field(ManagerProjectCommentNode,
                                     description="Get (or create for manager) the manager project comment on this "
                                                 "project review")

    def resolve_manager_comment(self, info):
        user = info.context.user
        return get_or_create_manager_project_comment(project_review=self, user=user)


class ManagerProjectCommentQuery(graphene.ObjectType):
    manager_project_comment = relay.Node.Field(ManagerProjectCommentNode)
    manager_project_comments = graphene.List(graphene.NonNull(ManagerProjectCommentNode), required=True)

    def resolve_manager_project_comments(self, info):
        return get_all_manager_project_comments(info.context.user)
