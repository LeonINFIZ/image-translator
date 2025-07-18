import uuid

from django.conf import settings
from django.db import models
from common.models import BaseModel


LANGUAGE_CHOICES = [
    ("uk", "Українська"),
    ("en", "Англійська"),
    ("de", "Німецька"),
    ("fr", "Французька"),
    ("es", "Іспанська"),
    ("it", "Італійська"),
    ("pl", "Польська"),
]


class TranslatedImage(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    image_hash = models.CharField(max_length=64, db_index=True)
    source_language = models.CharField(max_length=10, blank=True)
    target_language = models.CharField(max_length=10, default="uk", choices=LANGUAGE_CHOICES)

    original_image = models.FileField(upload_to="originals/")
    translated_image = models.FileField(upload_to="translated_images/")

    original_text_file = models.FileField(upload_to="original_texts/")
    translated_text_file = models.FileField(upload_to="translated_texts/")

    original_text = models.TextField(blank=True)
    translated_text = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "image_hash", "target_language")

    def __str__(self):
        return f"Translated Image {self.id} for {self.user.username} to '{self.get_target_language_display()}'"
