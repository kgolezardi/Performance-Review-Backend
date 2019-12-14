import graphene

import core.schema.project_query
import core.schema.person_review_query


class Query(
    core.schema.project_query.ProjectQuery,
    core.schema.person_review_query.PersonReviewQuery,
    graphene.ObjectType
):
    pass
