import graphene

from core.schema.adjust_project_review import AdjustProjectReviewMutation
from core.schema.create_project_review_mutation import CreateProjectReviewMutation
from core.schema.delete_project_review_mutation import DeleteProjectReviewMutation
from core.schema.save_manager_person_review_mutation import SaveManagerPersonReviewMutation
from core.schema.save_manager_project_comment_mutation import SaveManagerProjectCommentMutation
from core.schema.save_person_review_mutation import SavePersonReviewMutation
from core.schema.save_project_comment_mutation import SaveProjectCommentMutation
from core.schema.edit_project_review_mutation import EditProjectReviewMutation
from core.schema.start_review_mutation import StartReviewMutation


class Mutation(
    graphene.ObjectType,
):
    save_person_review = SavePersonReviewMutation.Field(required=True)
    create_project_review = CreateProjectReviewMutation.Field(required=True)
    edit_project_review = EditProjectReviewMutation.Field(required=True)
    delete_project_review = DeleteProjectReviewMutation.Field(required=True)
    adjust_project_review = AdjustProjectReviewMutation.Field(required=True)
    save_project_comment = SaveProjectCommentMutation.Field(required=True)
    save_manager_person_review = SaveManagerPersonReviewMutation.Field(required=True)
    save_manager_project_comment = SaveManagerProjectCommentMutation.Field(required=True)
    start_review = StartReviewMutation.Field(required=True)

