import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ..models import Project


class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        fields = ['name']
        filter_fields = {
            'name': ['exact', 'icontains']
        }
        interfaces = (relay.Node,)


class ProjectQuery(graphene.ObjectType):
    projects = DjangoFilterConnectionField(ProjectNode, required=True)
