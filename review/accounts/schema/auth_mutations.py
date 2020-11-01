import graphene

from .change_password_mutation import ChangePasswordMutation
from .login_mutation import LoginMutation
from .logout_mutation import LogoutMutation


class Mutation(
    graphene.ObjectType,
):
    login = LoginMutation.Field(required=True)
    logout = LogoutMutation.Field(required=True)
    change_password = ChangePasswordMutation.Field(required=True)
