import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        interfaces = (relay.Node,)

    @classmethod
    def base_query_set(cls, info):
        if info.context.user.is_authenticated:
            return User.objects.filter(is_staff=False, is_active=True)
        return User.objects.none()

    @classmethod
    def get_node(cls, info, id):
        try:
            return UserNode.base_query_set(info).get(id=id)
        except cls._meta.model.DoesNotExist:
            return None


class Query(graphene.ObjectType):
    users = graphene.List(UserNode, required=True)

    def resolve_users(self, info):
        return UserNode.base_query_set(info)

    user = relay.Node.Field(UserNode)
    me = graphene.Field(UserNode)

    def resolve_me(self, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
