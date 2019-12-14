import graphene

import core.schema.project_query
import core.schema.person_review_query
import core.schema.setting_query
import core.schema.project_review_query

class Query(
    core.schema.project_query.ProjectQuery,
    core.schema.person_review_query.PersonReviewQuery,
    core.schema.setting_query.SettingQuery,
    core.schema.project_review_query.ProjectReviewQuery,
    graphene.ObjectType
):
    pass
