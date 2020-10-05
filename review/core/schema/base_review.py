import graphene

from accounts.schema.user_query import UserNode


class BaseReview(graphene.Interface):
    reviewee = graphene.Field(UserNode, required=True)

