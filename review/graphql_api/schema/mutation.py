import graphene

import accounts.schema.auth_mutations


class Mutation(
    accounts.schema.auth_mutations.Mutation,
    graphene.ObjectType,
):
    pass
