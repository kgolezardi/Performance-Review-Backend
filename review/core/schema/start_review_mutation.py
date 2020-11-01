import graphene
from graphene import ClientIDMutation

from core.interactors.participation import start_review
from graphql_api.schema.with_viewer import WithViewer


class StartReviewMutation(WithViewer, ClientIDMutation):
    ok = graphene.NonNull(graphene.Boolean)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        user = info.context.user

        ok = start_review(user)
        return StartReviewMutation(ok=ok)
