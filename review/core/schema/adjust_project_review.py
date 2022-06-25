import graphene
from graphene import ClientIDMutation

from accounts.models import User
from core.interactors.project_review import adjust_project_review
from core.models import ProjectReview
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

        reviewers_id = args.get('reviewers_id', None)
        if reviewers_id is not None:
            reviewers = [get_node(reviewer_id, info, User) for reviewer_id in reviewers_id]
            reviewers = list(filter(None, reviewers))  # remove None values
        else:
            reviewers = None

        if project_review is None:
            return AdjustProjectReviewMutation(project_review=None)

        project_review = adjust_project_review(project_review, manager, reviewers=reviewers, **args)
        return AdjustProjectReviewMutation(project_review=project_review)
