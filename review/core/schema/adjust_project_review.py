import graphene
from graphene import ClientIDMutation

from core.interactors.project_review import adjust_project_review
from core.models import ProjectReview
from core.schema.utils import convert_ids_to_reviewers
from core.schema.project_review_query import ProjectReviewNode
from graphql_api.schema.utils import get_node
from graphql_api.schema.with_viewer import WithViewer


class AdjustProjectReviewMutation(WithViewer, ClientIDMutation):
    class Input:
        project_review_id = graphene.NonNull(graphene.ID)
        approved_by_manager = graphene.Boolean()
        reviewers_id = graphene.List(graphene.NonNull(graphene.ID))

    project_review = graphene.Field(ProjectReviewNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        project_review = get_node(args['project_review_id'], info, ProjectReview)
        manager = info.context.user
        reviewers = convert_ids_to_reviewers(args.pop('reviewers_id', None), info)

        if project_review is None:
            return AdjustProjectReviewMutation(project_review=None)

        project_review = adjust_project_review(project_review, manager, reviewers=reviewers, **args)
        return AdjustProjectReviewMutation(project_review=project_review)
