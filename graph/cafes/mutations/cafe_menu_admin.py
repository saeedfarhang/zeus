import graphene
from graphql import GraphQLError
from core.mutations.base_mutation import BaseMutation
from core.utils import create_thumbnails
from graph.core.enums import MenuErrorCode
from graph.core.types.upload import Upload
from graph.core.utils import add_hash_to_file_name, validate_image_file
from menu.models import Menu, MenuItem
from core.mutations.model_mutation import ModelMutation
from ..types import (
    MenuInput,
    MenuType,
    MenuItemInput,
    MenuItemType,
)
from ...core.types.common import MenuError


class MenuItemImageUpdate(BaseMutation):
    menuItem = graphene.Field(MenuType, description="An updated menu.")

    class Arguments:
        image = Upload(
            required=True,
            description="Represents an image file in a multipart request.",
        )

    class Meta:
        description = (
            "Create a menu image. This mutation must be sent "
            "as a `multipart` request. More detailed specs of the upload format can be "
            "found here: https://github.com/jaydenseric/graphql-multipart-request-spec"
        )
        error_type_class = MenuError
        permissions = ["sysadmin", "cafe"]

    @classmethod
    def perform_mutation(cls, _root, info, image):
        cafe = info.context.user.cafe

        image_data = info.context.FILES.get(image)
        validate_image_file(image_data, "image", MenuErrorCode)
        add_hash_to_file_name(image_data)
        if cafe.avatar:
            user.avatar.delete_sized_images()
            user.avatar.delete()
        user.avatar = image_data
        user.save()
        create_thumbnails.delay(user_id=user.pk)

        return MenuItemImageUpdate(user=user)


class MenuItemImageDelete(BaseMutation):
    menu_item = graphene.Field(MenuItem, description="An updated menu item instance.")

    class Meta:
        description = "Deletes a user avatar. Only for staff members."
        error_type_class = MenuError
        permissions = ["sysadmin"]

    @classmethod
    def perform_mutation(cls, _root, info):
        menuItem = info.context.user
        user.avatar.delete_sized_images()
        user.avatar.delete()
        return MenuItemImageDelete(user=user)


class CreateMenuAdmin(ModelMutation):
    class Arguments:
        input = MenuInput(required=True)

    class Meta:
        description = ("create menu.",)
        model = Menu
        object_type = MenuType
        error_type_class = MenuError
        permissions = ["sysadmin"]

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)

        cleaned_input = cls.get_input(data)
        instance = super().construct_instance(instance, cleaned_input)

        # create address
        super().save(info, instance, data)
        return super().success_response(instance)


class UpdateMenuAdmin(CreateMenuAdmin):
    @classmethod
    def instance_owner(cls, instance):
        return False

    class Arguments:
        id = graphene.ID(required=True, description="id of menu to be updated.")
        input = MenuInput(required=True, description="Fields required to update menu")

    class Meta:
        description = ("update a menu.",)
        model = Menu
        object_type = MenuType
        error_type_class = MenuError
        permissions = ["sysadmin", "menu"]

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        cleaned_input = cls.get_input(data)
        instance = super().construct_instance(instance, cleaned_input)
        super().save(info, instance, data)
        return super().success_response(instance)


class DeleteMenuAdmin(UpdateMenuAdmin):
    class Arguments:
        id = graphene.ID(required=True, description="id of menu to be deleted.")

    class Meta:
        description = ("delete a menu.",)
        model = Menu
        object_type = MenuType
        error_type_class = MenuError
        permissions = ["sysadmin", "menu"]

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        instance.delete()
        return super().success_response(instance)
