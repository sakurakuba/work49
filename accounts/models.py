from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from django.db import models

# Create your models here.


class Profile(models.Model):
    github = models.URLField(null=True, blank=True, verbose_name="GitHub")
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True, verbose_name="Avatar")
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name="user", related_name="profile")
    about = models.TextField(max_length=1000, null=True, blank=True, verbose_name='About')

    def __str__(self):
        return self.user.username + "'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
