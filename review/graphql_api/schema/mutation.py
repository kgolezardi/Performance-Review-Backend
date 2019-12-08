import graphene

import accounts.schema.auth_mutations
import core.schema.core_mutations


class Mutation(
    accounts.schema.auth_mutations.Mutation,
    core.schema.core_mutations.Mutation,
    graphene.ObjectType,
):
    pass
