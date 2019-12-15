from graphene import ObjectType, Boolean, Field


class Settings(ObjectType):
    self_assessment = Boolean(required=True)
    peer_reviews = Boolean(required=True)
    manager_reviews = Boolean(required=True)
    calibration = Boolean(required=True)
    result = Boolean(required=True)


class SettingQuery(ObjectType):
    settings = Field(Settings, required=True)

    def resolve_settings(self, info):
        return {
            "self_assessment": True,
            "peer_reviews": False,
            "manager_reviews": False,
            "calibration": False,
            "result": False,
        }
