import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.schema.user_query import UserNode
from core.interactors.settings import get_active_round
from core.schema.enums import Phase
from core.interactors.round import get_all_rounds, get_round
from core.models import Round
from core.schema.project_query import ProjectNode


class RoundNode(DjangoObjectType):
    class Meta:
        model = Round
        fields = [
            'title',
        ]
        interfaces = (relay.Node,)

    phase = Phase(required=True)
    projects = graphene.List(graphene.NonNull(ProjectNode), required=True)
    participants = graphene.List(graphene.NonNull(UserNode), required=True)

    def resolve_projects(self, info):
        return self.projects.all()

    def resolve_participants(self, info):
        return self.participants.all()

    @classmethod
    def get_node(cls, info, id):
        return get_round(info.context.user, id)


class RoundQuery(graphene.ObjectType):
    round = relay.Node.Field(RoundNode)
    active_round = graphene.Field(RoundNode)
    rounds = graphene.List(graphene.NonNull(RoundNode), required=True)

    def resolve_active_round(self, info):
        return get_active_round()

    def resolve_rounds(self, info):
        return get_all_rounds(info.context.user)
