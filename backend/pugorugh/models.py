from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    """This model represents a dog in the app."""
    name = models.CharField(max_length=200)
    image_filename = models.CharField(max_length=200)
    breed = models.CharField(
        max_length=200,
        default=""
        )
    age = models.IntegerField(
        help_text="integer for months")
    gender = models.CharField(
        help_text='"m" for male, "f" for female, "u" for unknown',
        max_length=1
        )
    size = models.CharField(
        help_text='s for small, "m" for medium, "l" for large, "xl" for extra large, "u" for unknown',
        max_length=2
        )
