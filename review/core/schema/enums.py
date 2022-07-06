import graphene

import core.enums

Evaluation = graphene.Enum.from_enum(core.enums.Evaluation)
Phase = graphene.Enum.from_enum(core.enums.Phase)
State = graphene.Enum.from_enum(core.enums.State)
QuestionType = graphene.Enum.from_enum(core.enums.QuestionType)
