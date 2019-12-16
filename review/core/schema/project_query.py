import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from core.interactors.project import get_all_projects, get_project
from ..models import Project


class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        fields = ['name']
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        return get_project(info.context.user)


class ProjectQuery(graphene.ObjectType):
    project = relay.Node.Field(ProjectNode)
    projects = graphene.List(graphene.NonNull(ProjectNode), required=True)

    def resolve_projects(self, info):
        return get_all_projects(info.context.user)
