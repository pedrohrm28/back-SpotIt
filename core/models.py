from django.conf import settings
from django.db import models


class Item(models.Model):
    class Status(models.TextChoices):
        LOST = "lost", "Perdido"
        FOUND = "found", "Encontrado"
        RETURNED = "returned", "Devolvido"

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.LOST,
    )
    category = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=255, blank=True)
    event_date = models.DateField(null=True, blank=True)
    image_url = models.URLField(blank=True)
    contact_info = models.CharField(max_length=255, blank=True)
    receiver_name = models.CharField(max_length=150, blank=True)
    receiver_contact = models.CharField(max_length=255, blank=True)
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reported_items",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.status})"
