from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    zip_code = models.CharField(max_length=5, default='00000')