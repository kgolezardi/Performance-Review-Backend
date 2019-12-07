from django.contrib.auth import logout
from graphene import ClientIDMutation

from graphql_api.schema.with_viewer import WithViewer


class LogoutMutation(WithViewer, ClientIDMutation):
    class Input:
        pass

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        logout(info.context)
        return LogoutMutation()
