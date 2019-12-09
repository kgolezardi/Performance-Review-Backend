import graphene

from core.schema.save_person_review_mutation import SavePersonReviewMutation


class Mutation(
    graphene.ObjectType,
):
    save_person_review = SavePersonReviewMutation.Field(required=True)
