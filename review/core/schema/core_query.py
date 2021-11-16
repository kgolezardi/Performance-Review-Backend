import graphene

import core.schema.person_review_query
import core.schema.setting_query
import core.schema.project_review_query
import core.schema.project_comment_query
import core.schema.manager_person_review_query
import core.schema.manager_project_comment_query
import core.schema.round_query
import core.schema.user_extensions


class Query(
    core.schema.person_review_query.PersonReviewQuery,
    core.schema.setting_query.SettingQuery,
    core.schema.project_review_query.ProjectReviewQuery,
    core.schema.project_comment_query.ProjectCommentQuery,
    core.schema.manager_person_review_query.ManagerPersonReviewQuery,
    core.schema.manager_project_comment_query.ManagerProjectCommentQuery,
    core.schema.round_query.RoundQuery,
    graphene.ObjectType
):
    pass
