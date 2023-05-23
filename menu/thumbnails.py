from ..celeryconf import app
from ..core.utils import create_thumbnails
from .models import User


@app.task
def create_menu_thumbnails(user_id):
    """Create thumbnails for user avatar."""
    create_thumbnails(
        pk=user_id, model=User, size_set="user_avatars", image_attr="avatar"
    )
