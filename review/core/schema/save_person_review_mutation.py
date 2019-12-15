import graphene
from graphene import ClientIDMutation

from accounts.models import User
from core.interactors.person_review import save_person_review
from core.schema.enums import Evaluation
from core.schema.person_review_query import PersonReviewNode
from graphql_api.schema.utils import get_node
from graphql_api.schema.with_viewer import WithViewer


class SavePersonReviewMutation(WithViewer, ClientIDMutation):
    class Input:
        reviewee_id = graphene.NonNull(graphene.ID)
        sahabiness_rating = Evaluation()
        sahabiness_comment = graphene.String()
        problem_solving_rating = Evaluation()
        problem_solving_comment = graphene.String()
        execution_rating = Evaluation()
        execution_comment = graphene.String()
        thought_leadership_rating = Evaluation()
        thought_leadership_comment = graphene.String()
        leadership_rating = Evaluation()
        leadership_comment = graphene.String()
        presence_rating = Evaluation()
        presence_comment = graphene.String()
        strengths = graphene.List(graphene.NonNull(graphene.String))
        weaknesses = graphene.List(graphene.NonNull(graphene.String))

    person_review = graphene.Field(PersonReviewNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        reviewee = get_node(args['reviewee_id'], info, User)
        reviewer = info.context.user

        if reviewee is None:
            return SavePersonReviewMutation(person_review=None)

        person_review = save_person_review(reviewee=reviewee, reviewer=reviewer, **args)
        return SavePersonReviewMutation(person_review=person_review)
