import graphene

from core.schema.project_review_query import ProjectReviewNode


class BaseProjectComment(graphene.Interface):
    project_review = graphene.Field(ProjectReviewNode, required=True)
