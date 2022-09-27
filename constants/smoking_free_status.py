from django.db.models import TextChoices


class SmokingFreeStatus(TextChoices):
    YES = "YES"
    NO = "NO"
    SMOKING_ROOM = "SMOKING_ROOM"
    SMOKING_SECTION = "SMOKING_SECTION"
