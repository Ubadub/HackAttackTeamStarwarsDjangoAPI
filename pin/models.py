from django.conf import settings
from django.db import models
from customauth.models import User

# Create your models here.

class Pin(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # coordinates, user

    class Meta:
        verbose_name = "Pin"
        verbose_name_plural = "Pins"

    def __str__(self):
        return verbose_name
    