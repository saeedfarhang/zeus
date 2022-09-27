import graphene
from django.core.exceptions import ValidationError
from django.http import *
from accounts.models import Role, User
from ..types import UserType, UserRoleType
from graphql_jwt.shortcuts import get_token, get_refresh_token, create_refresh_token
from graphql import GraphQLError


class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise GraphQLError("account does not exists")

        if user and user.check_password(password):
            token = get_token(user)
            refresh_token = create_refresh_token(user)

            return LoginUser(user=user, token=token, refresh_token=refresh_token)
        else:
            raise GraphQLError("account does not exists")


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = User(email=email)

        user.set_password(password)
        try:
            user.save()
        except:
            raise GraphQLError("this email is already exists.")

        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, token=token, refresh_token=refresh_token)
