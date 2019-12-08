import graphene

import core.schema.project_query


class Query(
    core.schema.project_query.ProjectQuery,
    graphene.ObjectType
):
    pass
