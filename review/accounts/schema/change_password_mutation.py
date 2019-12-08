import graphene
from graphene import ClientIDMutation

from graphql_api.schema.with_viewer import WithViewer


class ChangePasswordMutation(WithViewer, ClientIDMutation):
    class Input:
        old_password = graphene.NonNull(graphene.String)
        new_password = graphene.NonNull(graphene.String)

    ok = graphene.NonNull(graphene.Boolean)

    # TODO: Login requied
    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        old_password = args['old_password']
        new_password = args['new_password']

        user = info.context.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return ChangePasswordMutation(ok=True)

        return ChangePasswordMutation(ok=False)
