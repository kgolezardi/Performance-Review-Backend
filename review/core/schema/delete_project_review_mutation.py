import graphene
from graphene import ClientIDMutation

from core.interactors.project_review import delete_project_review
from core.models import ProjectReview
from core.schema.project_review_query import ProjectReviewNode
from graphql_api.schema.utils import get_node, get_node_global_id
from graphql_api.schema.with_viewer import WithViewer


class DeleteProjectReviewMutation(WithViewer, ClientIDMutation):
    class Input:
        project_review_id = graphene.NonNull(graphene.ID)

    deleted_project_review_id = graphene.ID()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        project_review = get_node(args['project_review_id'], info, ProjectReview)
        user = info.context.user

        if project_review is None:
            return DeleteProjectReviewMutation(deleted_project_review_id=None)

        project_review_id = delete_project_review(user, project_review)
        deleted_project_review_id = get_node_global_id(ProjectReviewNode, project_review_id)
        return DeleteProjectReviewMutation(deleted_project_review_id=deleted_project_review_id)
