from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
        max_length=150,
        unique=True,
        error_messages={
            "unique":"The email must be unique"
        }
    )
    profile_dp = models.ImageField(
        null = True, #DP can be null
        blank = True,
        upload_to = "profile_images"
    )
    REQUIRED_FIELDS= ["email"]
    objects = CustomUserManager

    def __str__(self):
        return self.username