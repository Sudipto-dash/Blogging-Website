import imp
from django.urls import path

from user_profile.views import login_user
from .views import *
urlpatterns = [
    path ('login/',login_user,name='login'),
    path ('signup/',signup_user,name='signup'),
    path ('logout/',logout_user,name='logout'),
    path ('profile/',user_profile,name='user_profile'),
    path ('change_profile_picture/',change_profile_picture,name='change_profile_picture'),
    path ('view_profile/<str:username>/',view_profile,name='view_profile'),
    path ('follow_or_unfollow_user/<int:user_id>/',follow_or_unfollow_user,name='follow_or_unfollow_user'),
    path ('user_notifications/',user_notifications,name='user_notifications'),
    path ('mute_or_unmute/<int:user_id>/',mute_or_unmute,name='mute_or_unmute'),
]