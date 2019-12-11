import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ..models import Project


class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        fields = ['name']
        interfaces = (relay.Node,)

    @classmethod
    def base_query_set(cls, info):
        # TODO move this logic to interactor
        if info.context.user.is_authenticated:
            return Project.objects.all()
        return Project.objects.none()

    @classmethod
    def get_node(cls, info, id):
        try:
            return ProjectNode.base_query_set(info).get(id=id)
        except cls._meta.model.DoesNotExist:
            return None


class ProjectQuery(graphene.ObjectType):
    project = relay.Node.Field(ProjectNode)
    projects = graphene.List(graphene.NonNull(ProjectNode), required=True)

    def resolve_projects(self, info):
        return ProjectNode.base_query_set(info)
