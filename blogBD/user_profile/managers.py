import imp
from pickle import TRUE
from django.contrib.auth.base_user import BaseUserManager
from matplotlib.style import use

class CustomUserManager(BaseUserManager):
    def create_user(self,username,email,password,**extra_fields):
        if not username:
            raise ValueError("The user must set")
        if not email:
            raise ValueError("The email must set")
        if not password:
            raise ValueError("The password must set")
        email = self.normalize_email(email)
        user =  self.model(
            username,
            email,
            password,
            **extra_fields
        )
        user.set_password(password)
        user.save()   
        return user

    def create_superuser(self,username,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get ('is_staff') is not TRUE:
            raise ValueError ("The Super Users must have is_staff = True")
        if extra_fields.get ('is_superuser') is not TRUE:
            raise ValueError ("The Super Users must have is_superuser = True")

        return self.create_user(
            username,email,password,**extra_fields
        )    