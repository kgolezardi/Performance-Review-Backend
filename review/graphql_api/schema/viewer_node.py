import graphene

import accounts.schema.user_query
import core.schema.core_query
from graphql_api.schema.utils import get_node


class ViewerNode(
    core.schema.core_query.Query,
    accounts.schema.user_query.Query,
    graphene.ObjectType,
):
    class Meta:
        interfaces = (graphene.relay.Node,)

    node = graphene.Field(graphene.relay.Node, id=graphene.NonNull(graphene.ID))

    def resolve_node(self, info, id):
        return get_node(global_id=id, info=info)

    @classmethod
    def get_node(cls, id, info):
        if id == "0":
            return ViewerNode(id=id)
        return None
