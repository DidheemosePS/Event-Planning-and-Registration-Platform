from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    is_organization = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=False)
