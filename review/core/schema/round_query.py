import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from accounts.schema.user_query import UserNode
from core.interactors.round import get_all_rounds, get_round
from core.interactors.settings import get_active_round
from core.models import Round
from core.schema.enums import Phase


class RoundNode(DjangoObjectType):
    class Meta:
        model = Round
        fields = [
            'title',
            'max_project_reviews',
            'max_reviewers',
            'self_review_project_fields',
            'peer_review_project_fields',
            'manager_review_project_fields',
            'private_manager_review_project_fields',
        ]
        interfaces = (relay.Node,)

    phase = Phase(required=True)
    participants = graphene.List(graphene.NonNull(UserNode), required=True)

    def resolve_participants(self, info):
        return self.participants.all()

    @classmethod
    def get_node(cls, info, id):
        return get_round(info.context.user, id)


class RoundQuery(graphene.ObjectType):
    round = relay.Node.Field(RoundNode)
    active_round = graphene.NonNull(RoundNode)
    rounds = graphene.List(graphene.NonNull(RoundNode), required=True)

    def resolve_active_round(self, info):
        return get_active_round()

    def resolve_rounds(self, info):
        return get_all_rounds(info.context.user)
