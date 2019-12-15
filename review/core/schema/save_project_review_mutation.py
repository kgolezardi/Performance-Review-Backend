import graphene
from graphene import ClientIDMutation

from accounts.models import User
from core.interactors import save_project_review
from core.models import Project
from core.schema.enums import Evaluation
from core.schema.project_review_query import ProjectReviewNode
from graphql_api.schema.utils import get_node
from graphql_api.schema.with_viewer import WithViewer


class SaveProjectReviewMutation(WithViewer, ClientIDMutation):
    class Input:
        project_id = graphene.NonNull(graphene.ID)
        text = graphene.String()
        rating = Evaluation()
        reviewers_id = graphene.List(graphene.NonNull(graphene.ID))

    project_review = graphene.Field(ProjectReviewNode)

    # TODO: Login requied
    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        project = get_node(args['project_id'], info, Project)
        reviewee = info.context.user

        reviewers = None
        if 'reviewers_id' in args and args['reviewers_id'] is not None:
            reviewers = [get_node(reviewer_id, info, User) for reviewer_id in args['reviewers_id']]
            reviewers = list(filter(None, reviewers))  # remove None values
            if reviewee in reviewers:
                reviewers.remove(reviewee)

        if project is None:
            return SaveProjectReviewMutation(project_review=None)

        project_review = save_project_review(project, reviewee, reviewers, **args)
        return SaveProjectReviewMutation(project_review=project_review)
