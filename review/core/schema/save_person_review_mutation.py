import graphene
from graphene import ClientIDMutation

from accounts.models import User
from core.interactors.person_review import save_person_review
from core.schema.enums import Evaluation, State
from core.schema.person_review_query import PersonReviewNode
from graphql_api.schema.utils import get_node
from graphql_api.schema.with_viewer import WithViewer


class SavePersonReviewMutation(WithViewer, ClientIDMutation):
    class Input:
        reviewee_id = graphene.NonNull(graphene.ID)
        strengths = graphene.List(graphene.NonNull(graphene.String))
        weaknesses = graphene.List(graphene.NonNull(graphene.String))
        state = State()

    person_review = graphene.Field(PersonReviewNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        reviewee = get_node(args['reviewee_id'], info, User)
        reviewer = info.context.user

        if reviewee is None:
            return SavePersonReviewMutation(person_review=None)

        person_review = save_person_review(reviewee=reviewee, reviewer=reviewer, **args)
        return SavePersonReviewMutation(person_review=person_review)
