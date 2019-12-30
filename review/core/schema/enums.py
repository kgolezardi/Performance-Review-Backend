import graphene

import core.enums

Evaluation = graphene.Enum.from_enum(core.enums.Evaluation)
Phase = graphene.Enum.from_enum(core.enums.Phase)
