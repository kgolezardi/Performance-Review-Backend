import graphene
from graphene import ClientIDMutation

from accounts.interactors.user import change_password
from graphql_api.schema.with_viewer import WithViewer


class ChangePasswordMutation(WithViewer, ClientIDMutation):
    class Input:
        old_password = graphene.NonNull(graphene.String)
        new_password = graphene.NonNull(graphene.String)

    ok = graphene.NonNull(graphene.Boolean)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        old_password = args['old_password']
        new_password = args['new_password']
        user = info.context.user

        ok = change_password(user, old_password, new_password)
        return ChangePasswordMutation(ok=ok)
