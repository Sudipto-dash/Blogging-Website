from distutils.command.upload import upload
from tkinter import CASCADE
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

    followers = models.ManyToManyField("Follow")
    REQUIRED_FIELDS= ["email"]
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    def get_profile_picture(self):
        url = ""
        try:
            url = self.profile_dp.url
        except:
            url = ""
        return url

#Social Model   
class Follow(models.Model):
    followed = models.ForeignKey( #who is followed by others
        User,
        related_name='user_followers',
        on_delete=models.CASCADE
    )
    followed_by = models.ForeignKey( #who follows
        User,
        related_name='user_follows',
        on_delete=models.CASCADE
    )
    muted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.followed_by.username} started following {self.followed.username}"