import graphene

from accounts.models.role import User

from .types import UserType

class AccountQueries(graphene.ObjectType):
    me = graphene.Field(UserType, description="Return the currently authenticated user.")
    users = graphene.List(UserType)

    @staticmethod
    def resolve_me(root, info):
        user = info.context.user

        return user if user.is_authenticated else None

    @staticmethod
    def resolve_users(root, info):
        user = info.context.user
        if user.role.role == 'sysadmin':
            return User.objects.all()
        else:
           raise Exception('Authentication Failure: Must be Manager')


        