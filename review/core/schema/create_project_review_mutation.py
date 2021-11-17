import graphene
from graphene import ClientIDMutation

from core.interactors.project_review import create_project_review
from core.schema.project_review_query import ProjectReviewNode
from graphql_api.schema.with_viewer import WithViewer


class CreateProjectReviewMutation(WithViewer, ClientIDMutation):
    class Input:
        project_name = graphene.String()

    project_review = graphene.Field(ProjectReviewNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        reviewee = info.context.user
        project_name = args.get('project_name', None)
        project_review = create_project_review(project_name, reviewee)
        return CreateProjectReviewMutation(project_review=project_review)
