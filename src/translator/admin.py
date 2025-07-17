from .models import TranslatedImage
from django.contrib import admin


@admin.register(TranslatedImage)
class TranslatedImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image_hash", "target_language", "created_at")
    readonly_fields = ("id", "created_at", "image_hash", "original_text", "translated_text")
    list_filter = ("target_language",)
    search_fields = ("image_hash",)
