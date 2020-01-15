import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from core.interactors.settings import get_settings
from core.models import Settings
from core.schema.enums import Phase


class SettingsNode(DjangoObjectType):
    class Meta:
        model = Settings
        fields = ['due_date', 'login_background_image']
        interfaces = (relay.Node,)

    phase = Phase(required=True)


class SettingQuery(ObjectType):
    settings = graphene.Field(SettingsNode, required=True)

    def resolve_settings(self, info):
        return get_settings()
