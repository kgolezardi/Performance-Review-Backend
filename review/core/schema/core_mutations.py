import graphene

from core.schema.delete_project_review_mutation import DeleteProjectReviewMutation
from core.schema.finalize_submission_mutation import FinalizeSubmissionMutation
from core.schema.save_person_review_mutation import SavePersonReviewMutation
from core.schema.save_project_comment_mutation import SaveProjectCommentMutation
from core.schema.save_project_review_mutation import SaveProjectReviewMutation


class Mutation(
    graphene.ObjectType,
):
    save_person_review = SavePersonReviewMutation.Field(required=True)
    save_project_review = SaveProjectReviewMutation.Field(required=True)
    delete_project_review = DeleteProjectReviewMutation.Field(required=True)
    finalize_submission = FinalizeSubmissionMutation.Field(required=True)
    save_project_comment = SaveProjectCommentMutation.Field(required=True)
