import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.interactors import get_all_users, get_user, is_valid_user
from ..models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'avatar_url']
        interfaces = (relay.Node,)

    is_manager = graphene.Boolean(required=True)

    def resolve_is_manager(self, info):
        return self.is_manager

    @classmethod
    def get_node(cls, info, id):
        return get_user(info.context.user, id)


class Query(graphene.ObjectType):
    users = graphene.List(graphene.NonNull(UserNode), required=True)

    def resolve_users(self, info):
        return get_all_users(info.context.user)

    user = relay.Node.Field(UserNode)
    me = graphene.Field(UserNode)

    def resolve_me(self, info):
        if is_valid_user(info.context.user):
            return info.context.user
        return None
