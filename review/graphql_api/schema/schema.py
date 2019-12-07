import graphene

from graphql_api.schema.mutation import Mutation
from graphql_api.schema.query import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
