import graphene

from accounts.schema.user_query import UserNode
from core.interactors.authorization import can_view_ranking
from core.interactors.participation import has_user_started
from graphql_api.schema.extension import Extension


class UserNodeParticipationExtension(Extension):
    class Meta:
        base = UserNode

    has_started = graphene.Boolean(required=False)

    def resolve_has_started(self, info):
        if info.context.user == self:
            return has_user_started(self)
        return None


class UserNodeRankingExtension(Extension):
    class Meta:
        base = UserNode

    ranking1 = graphene.Field(graphene.String)
    ranking2 = graphene.Field(graphene.String)

    def resolve_ranking1(self, info):
        if can_view_ranking(info.context.user, self):
            return self.ranking1
        return None

    def resolve_ranking2(self, info):
        if can_view_ranking(info.context.user, self):
            return self.ranking2
        return None
