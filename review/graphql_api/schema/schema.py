import graphene

from graphql_api.schema.query import Query

schema = graphene.Schema(
    query=Query,
)
