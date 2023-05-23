from .jwt_payload import jwt_payload
from .allow_any import allow_any
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from celery.utils.log import get_task_logger

task_logger = get_task_logger(__name__)


def snake_to_camel_case(name):
    """Convert snake_case variable name to camelCase."""
    if isinstance(name, str):
        split_name = name.split("_")
        return split_name[0] + "".join(map(str.capitalize, split_name[1:]))
    return name


def create_thumbnails(pk, model, size_set, image_attr=None):
    instance = model.objects.get(pk=pk)
    if not image_attr:
        image_attr = "image"
    image_instance = getattr(instance, image_attr)
    if image_instance.name == "":
        # There is no file, skip processing
        return
    warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance, rendition_key_set=size_set, image_attr=image_attr
    )
    task_logger.info("Creating thumbnails for %s", pk)
    num_created, failed_to_create = warmer.warm()
    if num_created:
        task_logger.info("Created %d thumbnails", num_created)
    if failed_to_create:
        task_logger.error(
            "Failed to generate thumbnails", extra={"paths": failed_to_create}
        )
