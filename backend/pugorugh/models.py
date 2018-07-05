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
    user_pref_age = models.CharField(
        help_text='"b" for baby, "y" for young, "a" for adult, "s" for senior',
        max_length=2
        )
    gender = models.CharField(
        help_text='"m" for male, "f" for female, "u" for unknown',
        max_length=1
        )
    size = models.CharField(
        help_text='s for small, "m" for medium, '
                  '"l" for large, "xl" for extra large, "u" for unknown',
        max_length=2
        )

    def save(self, *args, **kwargs):
        """Groups dogs by configurable user preferences"""
        # NOTE: Data must loaded after model is created to ensure rule runs
        if self.age <= 12:
            self.user_pref_age = "b"
        elif self.age <= 36:
            self.user_pref_age = "y"
        elif self.age <= 64:
            self.user_pref_age = "a"
        elif self.age > 64:
            self.user_pref_age = "s"
        else:
            self.user_pref_age = "u"
        super(Dog, self).save(*args, **kwargs)


class UserDog(models.Model):
    """This model represents a link between a user an a dog"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="id"
        )
    dog = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        verbose_name="id"
        )
    status = models.CharField(
        help_text='“l” for liked, “d” for disliked',
        max_length=1,
        default="u"
        )


class UserPref(models.Model):
    """This model contains the user's preferences"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="id"
        )
    age = models.CharField(
        help_text='"b" for baby, "y" for young, "a" for adult, "s" for senior',
        max_length=1,
        default="b,y,a,s"
        )
    gender = models.CharField(
        help_text='"m" for male, "f" for female, "u" for unknown',
        max_length=1,
        default="f,m"
        )
    size = models.CharField(
        help_text='s for small, "m" for medium, '
                  '"l" for large, "xl" for extra large',
        max_length=2,
        default="s,m,l,xl"
        )
