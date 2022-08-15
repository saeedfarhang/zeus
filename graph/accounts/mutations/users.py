import graphene
from django.core.exceptions import ValidationError
from django.http import *
from accounts.models import Role, User
from ..types import UserType, UserRoleType
from graphql_jwt.shortcuts import get_token, get_refresh_token, create_refresh_token


class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    role = graphene.Field(UserRoleType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({
                "error":"email does not exists"
            })

        if user and user.check_password(password):
            role = Role.objects.get(user=user.id)
            token = get_token(user)
            refresh_token = create_refresh_token(user)

            return CreateUser(user=user, role=role, token=token, refresh_token=refresh_token)
        else:
            return None


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    role = graphene.Field(UserRoleType)
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
            raise ValidationError(message='this email is already exists.', code=http)
        
        role = Role.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, role=role, token=token, refresh_token=refresh_token)