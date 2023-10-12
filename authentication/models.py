from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_photo = models.ImageField(verbose_name='photo de profil')
    follows = models.ManyToManyField( 'self', 
                                     symmetrical=True,
                                     verbose_name='suit'
    )

