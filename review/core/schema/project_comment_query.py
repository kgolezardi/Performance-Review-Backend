import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.schema.user_query import UserNode
from core.interactors.project_comment import get_all_project_comments, get_project_comment, get_project_review_comments, \
    get_or_create_project_comment, get_project_comment_reviewer, get_project_comment_answers
from core.schema.enums import Evaluation
from graphql_api.schema.extension import Extension
from .answer_types import AnswerOutput
from .project_review_query import ProjectReviewNode
from ..models import ProjectComment


class ProjectCommentNode(DjangoObjectType):
    class Meta:
        model = ProjectComment
        fields = [
            'project_review',
        ]
        interfaces = (relay.Node,)

    reviewer = graphene.Field(UserNode)
    rating = Evaluation()
    answers = graphene.List(graphene.NonNull(AnswerOutput), required=True)

    def resolve_reviewer(self, info):
        user = info.context.user
        return get_project_comment_reviewer(user, self)

    def resolve_answers(self, info):
        return get_project_comment_answers(self)

    @classmethod
    def get_node(cls, info, id):
        return get_project_comment(info.context.user, id)


class ProjectReviewNodeCommentsExtension(Extension):
    class Meta:
        base = ProjectReviewNode

    comment = graphene.Field(ProjectCommentNode,
                             description="Get or create a project comment about this project review from the logged "
                                         "in user")
    comments = graphene.List(graphene.NonNull(ProjectCommentNode), required=True)

    def resolve_comment(self, info):
        reviewer = info.context.user
        return get_or_create_project_comment(project_review=self, reviewer=reviewer)

    def resolve_comments(self, info):
        return get_project_review_comments(info.context.user, self)


class ProjectCommentQuery(graphene.ObjectType):
    project_comment = relay.Node.Field(ProjectCommentNode)
    project_comments = graphene.List(graphene.NonNull(ProjectCommentNode), required=True)

    def resolve_project_comments(self, info):
        return get_all_project_comments(info.context.user)
