from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings

# Create your models here.
class User(AbstractUser):
    zip_code = models.CharField(max_length=5, default="00000")
    profile_photo = models.ImageField(verbose_name="photo de profil", upload_to="auth/profile_photo", blank=True, null=True, default="auth/profile_photo/default.png")
    # follows = models.ManyToManyField("self", symmetrical=True, verbose_name="suit")
    # subscribers = models.ManyToManyField("self", symmetrical=False, verbose_name="abonnés", blank=True)



