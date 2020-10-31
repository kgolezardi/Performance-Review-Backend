import graphene

from accounts.schema.user_query import UserNode
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
