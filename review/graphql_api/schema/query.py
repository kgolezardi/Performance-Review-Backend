import graphene

from graphql_api.schema.with_viewer import WithViewer


class Query(graphene.ObjectType, WithViewer):
    pass
