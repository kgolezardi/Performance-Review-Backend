import graphene
from django.contrib.auth import authenticate, login
from graphene import ClientIDMutation

from graphql_api.schema.with_viewer import WithViewer
from .user_query import UserNode


class LoginMutation(WithViewer, ClientIDMutation):
    class Input:
        username = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **args):
        username = args['username']
        password = args['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return LoginMutation(user=None)
        if not user.is_active:
            return LoginMutation(user=None)

        login(info.context, user)
        return LoginMutation(user=user)
