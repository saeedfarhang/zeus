from typing import TYPE_CHECKING
import graphene
from django.core.exceptions import (
    NON_FIELD_ERRORS,
    ImproperlyConfigured,
    ValidationError,
)
from django.db.models.fields.files import FileField
from graphene.types.mutation import MutationOptions


from core.utils import snake_to_camel_case
from graph.core.types.common import NonNullList
from graph.core.utils.error_codes import get_error_code_from_error


def get_error_fields(error_type_class, error_type_field, deprecation_reason=None):
    error_field = graphene.Field(
        NonNullList(
            error_type_class,
            description="List of errors that occurred executing the mutation.",
        ),
        default_value=[],
        required=True,
    )
    if deprecation_reason is not None:
        error_field.deprecation_reason = deprecation_reason
    return {error_type_field: error_field}


def attach_error_params(error, params: dict, error_class_fields: set):
    if not params:
        return {}
    # If some of the params key overlap with error class fields
    # attach param value to the error
    error_fields_in_params = set(params.keys()) & error_class_fields
    for error_field in error_fields_in_params:
        setattr(error, error_field, params[error_field])


def validation_error_to_error_type(
    validation_error: ValidationError, error_type_class
) -> list:
    """Convert a ValidationError into a list of Error types."""
    err_list = []
    error_class_fields = set(error_type_class._meta.fields.keys())
    if hasattr(validation_error, "error_dict"):
        # convert field errors
        for field, field_errors in validation_error.error_dict.items():
            field = None if field == NON_FIELD_ERRORS else snake_to_camel_case(field)
            for err in field_errors:
                error = error_type_class(
                    field=field,
                    message=err.messages[0],
                    code=get_error_code_from_error(err),
                )
                attach_error_params(error, err.params, error_class_fields)
                err_list.append(error)
    else:
        # convert non-field errors
        for err in validation_error.error_list:
            error = error_type_class(
                message=err.messages[0],
                code=get_error_code_from_error(err),
            )
            attach_error_params(error, err.params, error_class_fields)
            err_list.append(error)
    return err_list


class BaseMutation(graphene.Mutation):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        description=None,
        _meta=None,
        error_type_class=None,
        error_type_field=None,
        errors_mapping=None,
        permissions=None,
        **options,
    ):
        if not _meta:
            _meta = MutationOptions(cls)

        if not description:
            raise ImproperlyConfigured("No description provided in Meta")

        if not error_type_class:
            raise ImproperlyConfigured("No error_type_class provided in Meta.")

        _meta.error_type_class = error_type_class
        _meta.error_type_field = error_type_field
        _meta.errors_mapping = errors_mapping
        _meta.permissions = permissions

        super().__init_subclass_with_meta__(
            description=description, _meta=_meta, **options
        )

        cls._meta.fields.update(get_error_fields(error_type_class, "errors"))

    @classmethod
    def _update_mutation_arguments_and_fields(cls, arguments, fields):
        cls._meta.arguments.update(arguments)
        cls._meta.fields.update(fields)

    @staticmethod
    def remap_error_fields(validation_error, field_map):
        """Rename validation_error fields according to provided field_map.

        Skips renaming fields from field_map that are not on validation_error.
        """
        for old_field, new_field in field_map.items():
            try:
                validation_error.error_dict[
                    new_field
                ] = validation_error.error_dict.pop(old_field)
            except KeyError:
                pass

    @classmethod
    def has_permission(cls, info):
        try:
            if cls._meta.permissions.__contains__(info.context.user.role.role):
                return True
            raise Exception("permission denied")
        except:
            raise Exception("permission denied")

    @classmethod
    def clean_instance(cls, info, instance):
        """Clean the instance that was created using the input data.

        Once an instance is created, this method runs `full_clean()` to perform
        model validation.
        """
        try:
            instance.full_clean()
        except ValidationError as error:
            if hasattr(cls._meta, "exclude"):
                # Ignore validation errors for fields that are specified as
                # excluded.
                new_error_dict = {}
                for field, errors in error.error_dict.items():
                    if field not in cls._meta.exclude:
                        new_error_dict[field] = errors
                error.error_dict = new_error_dict

            if cls._meta.errors_mapping:
                cls.remap_error_fields(error, cls._meta.errors_mapping)

            if error.error_dict:
                raise error

    @classmethod
    def construct_instance(cls, instance, cleaned_data):
        """Fill instance fields with cleaned data.

        The `instance` argument is either an empty instance of a already
        existing one which was fetched from the database. `cleaned_data` is
        data to be set in instance fields. Returns `instance` with filled
        fields, but not saved to the database.
        """
        from django.db import models

        opts = instance._meta

        for f in opts.fields:
            if any(
                [
                    not f.editable,
                    isinstance(f, models.AutoField),
                    f.name not in cleaned_data,
                ]
            ):
                continue
            data = cleaned_data[f.name]
            if data is None:
                # We want to reset the file field value when None was passed
                # in the input, but `FileField.save_form_data` ignores None
                # values. In that case we manually pass False which clears
                # the file.
                if isinstance(f, FileField):
                    data = False
                if not f.null:
                    data = f._get_default()
            f.save_form_data(instance, data)
        return instance

    @classmethod
    def mutate(cls, root, info, **data):
        # set_mutation_flag_in_context(info.context)

        # result = info.context.plugins.perform_mutation(
        #     mutation_cls=cls, root=root, info=info, data=data
        # )
        # if result is not None:
        #     return result
        cls.has_permission(info)
        try:
            response = cls.perform_mutation(root, info, **data)
            if response.errors is None:
                response.errors = []
            return response
        except ValidationError as e:
            return cls.handle_errors(e)

    @classmethod
    def perform_mutation(cls, _root, _info, **data):
        pass

    @classmethod
    def handle_errors(cls, error: ValidationError, **extra):
        error_list = validation_error_to_error_type(error, cls._meta.error_type_class)
        return cls.handle_typed_errors(error_list, **extra)

    @classmethod
    def handle_typed_errors(cls, errors: list, **extra):
        """Return class instance with errors."""
        if cls._meta.error_type_field is not None:
            extra.update({cls._meta.error_type_field: errors})
        return cls(errors=errors, **extra)


if TYPE_CHECKING:
    from django.http import HttpRequest


def set_mutation_flag_in_context(context: "HttpRequest"):
    """Set information in context to don't use database replicas.

    Part of the database read replicas in Saleor.
    When Saleor builds a response for mutation `context` stores information
    `is_mutation=True`. That means that all data should be provided from
    the master database.
    When Saleor build a response for query `context` doesn’t have the
    `is_mutation` field.
    That means that all data should be provided from reading replica of the database.
    Database read replica couldn't be used to save any data.
    """
    context.is_mutation = True  # type: ignore
