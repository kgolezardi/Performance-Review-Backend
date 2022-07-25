import graphene
from graphene import ObjectType, relay
from graphene_django import DjangoObjectType

from core.interactors.authorization import can_view_manager_overall_review_text
from core.interactors.settings import get_settings
from core.models import Settings
from core.schema.enums import Phase


class SettingsNode(DjangoObjectType):
    class Meta:
        model = Settings
        fields = ['login_background_image', 'idle_page_url', 'logo_url', 'light_logo_url']
        interfaces = (relay.Node,)

    phase = Phase(required=True)
    start_text = graphene.Field(graphene.String)
    manager_overall_review_text = graphene.Field(graphene.String)

    def resolve_phase(self, info):
        return self.active_round.phase

    def resolve_start_text(self, info):
        return self.active_round.start_text

    def resolve_manager_overall_review_text(self, info):
        if can_view_manager_overall_review_text(info.context.user):
            return self.active_round.manager_overall_review_text
        return None


class SettingQuery(ObjectType):
    settings = graphene.Field(SettingsNode, required=True)

    def resolve_settings(self, info):
        return get_settings()
