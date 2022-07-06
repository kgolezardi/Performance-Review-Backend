import graphene
from graphene import ClientIDMutation

from core.interactors.project_review import edit_project_review
from core.models import ProjectReview
from core.schema.answer_types import AnswerInput
from core.schema.enums import Evaluation
from core.schema.utils import convert_ids_to_reviewers, convert_answers_input
from core.schema.project_review_query import ProjectReviewNode
from graphql_api.schema.utils import get_node
from graphql_api.schema.with_viewer import WithViewer


class EditProjectReviewMutation(WithViewer, ClientIDMutation):
    class Input:
        project_review_id = graphene.NonNull(graphene.ID)
        project_name = graphene.String()
        answers = graphene.List(graphene.NonNull(AnswerInput))
        rating = Evaluation()
        consulted_with_manager = graphene.Boolean()
        reviewers_id = graphene.List(graphene.NonNull(graphene.ID))

    project_review = graphene.Field(ProjectReviewNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        project_review = get_node(args['project_review_id'], info, ProjectReview)
        reviewee = info.context.user
        reviewers = convert_ids_to_reviewers(args.pop('reviewers_id', None), info)
        answers = convert_answers_input(args.pop('answers', None), info)

        if project_review is None:
            return EditProjectReviewMutation(project_review=None)

        project_review = edit_project_review(project_review, reviewee, reviewers=reviewers, answers=answers, **args)
        return EditProjectReviewMutation(project_review=project_review)
