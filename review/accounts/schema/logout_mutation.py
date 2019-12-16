from django.contrib.auth import logout
from graphene import ClientIDMutation

from graphql_api.schema.with_viewer import WithViewer


class LogoutMutation(WithViewer, ClientIDMutation):
    class Input:
        pass

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        if info.context.user.is_authenticated:
            logout(info.context)
        return LogoutMutation()
