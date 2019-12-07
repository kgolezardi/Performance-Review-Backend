from graphene import AbstractType, Field

from graphql_api.schema.viewer_node import ViewerNode


class WithViewer(AbstractType):
    viewer = Field(ViewerNode, required=True)

    def resolve_viewer(self, info):
        return ViewerNode(id="0")
