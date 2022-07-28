import graphene
from graphene import ClientIDMutation

from accounts.models import User
from core.interactors.manager_person_review import save_manager_person_review
from core.schema.enums import Evaluation
from core.schema.manager_person_review_query import ManagerPersonReviewNode
from graphql_api.schema.utils import get_node
from graphql_api.schema.with_viewer import WithViewer


class SaveManagerPersonReviewMutation(WithViewer, ClientIDMutation):
    class Input:
        reviewee_id = graphene.NonNull(graphene.ID)
        strengths = graphene.List(graphene.NonNull(graphene.String))
        weaknesses = graphene.List(graphene.NonNull(graphene.String))
        overall_rating = Evaluation()

    manager_person_review = graphene.Field(ManagerPersonReviewNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        reviewee = get_node(args['reviewee_id'], info, User)
        manager = info.context.user

        if reviewee is None:
            return SaveManagerPersonReviewMutation(manager_person_review=None)

        manager_person_review = save_manager_person_review(reviewee=reviewee, manager=manager, **args)
        return SaveManagerPersonReviewMutation(manager_person_review=manager_person_review)
