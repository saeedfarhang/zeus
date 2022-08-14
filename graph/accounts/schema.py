import graphene

from .types import UserType

class AccountQueries (graphene.ObjectType):
    me = graphene.Field(UserType, description="Return the currently authenticated user.")

    @staticmethod
    def resolve_me(root, info):
        user = info.context.user

        return user if user.is_authenticated else None