import graphene
from graphene import ClientIDMutation

from core.interactors.project_comment import save_project_comment
from core.models import ProjectReview
from core.schema.answer_types import AnswerInput
from core.schema.enums import Evaluation
from core.schema.project_comment_query import ProjectCommentNode
from core.schema.utils import convert_answers_input
from graphql_api.schema.utils import get_node
from graphql_api.schema.with_viewer import WithViewer


class SaveProjectCommentMutation(WithViewer, ClientIDMutation):
    class Input:
        project_review_id = graphene.NonNull(graphene.ID)
        answers = graphene.List(graphene.NonNull(AnswerInput))
        rating = Evaluation()

    project_comment = graphene.Field(ProjectCommentNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        project_review = get_node(args['project_review_id'], info, ProjectReview)
        user = info.context.user
        answers = convert_answers_input(args.pop('answers', None), info)

        if project_review is None:
            return SaveProjectCommentMutation(project_comment=None)

        project_comment = save_project_comment(project_review, user, answers=answers, **args)
        return SaveProjectCommentMutation(project_comment=project_comment)
