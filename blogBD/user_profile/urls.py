import imp
from django.urls import path

from user_profile.views import login_user
from .views import *
urlpatterns = [
    path ('login/',login_user,name='login'),
    path ('signup/',signup_user,name='signup'),
    path ('logout/',logout_user,name='logout'),
]