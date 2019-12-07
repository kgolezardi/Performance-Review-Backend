import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ..models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        filter_fields = ['username']
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    users = DjangoFilterConnectionField(UserNode, required=True)
    user = relay.Node.Field(UserNode)
    me = graphene.Field(UserNode)

    def resolve_me(self, info):
        if info.context.user and info.context.user.is_authenticated:
            return info.context.user
        return None
