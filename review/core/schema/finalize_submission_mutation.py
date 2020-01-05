import graphene
from graphene import ClientIDMutation

from accounts.models import User
from core.interactors.person_review import finalize_submission
from core.schema.person_review_query import PersonReviewNode
from graphql_api.schema.utils import get_node
from graphql_api.schema.with_viewer import WithViewer


class FinalizeSubmissionMutation(WithViewer, ClientIDMutation):
    class Input:
        reviewee_id = graphene.NonNull(graphene.ID)

    person_review = graphene.Field(PersonReviewNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        reviewee = get_node(args['reviewee_id'], info, User)
        reviewer = info.context.user

        if reviewee is None:
            return FinalizeSubmissionMutation(person_review=None)

        person_review = finalize_submission(reviewee=reviewee, reviewer=reviewer)
        return FinalizeSubmissionMutation(person_review=person_review)
