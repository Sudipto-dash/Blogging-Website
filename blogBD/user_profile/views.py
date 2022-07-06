import imp
import re
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from matplotlib.style import context
from django.views.decorators.cache import never_cache
from pyparsing import FollowedBy
from .forms import (
    userSignUpForm,
    loginForm,
    UserProfileUpdateForm,
    ProfilePictureUpdateForm
)
from notification.models import Notifications, Notifications
from .models import User,Follow
from .decorators import (
    not_logged_in_required
)
#LogIn
@not_logged_in_required
@never_cache #not caching the page after login
def login_user(request):
    form = loginForm()

    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password')
            )
            if user:
                login(request,user)
                return redirect ('home')
            else:
                messages.warning(request, "Invalid Credentials")
    context= {
        "form" : form
    }
    return render(request,'login.html',context)

#LogOut
def logout_user(request):
    logout(request)
    return redirect('login')

#Registration
@not_logged_in_required
@never_cache
def signup_user(request):
    form = userSignUpForm()
    if request.method == "POST":
        form = userSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request,"Sign Up completed")
            return redirect('login')

    context= {
        "form" : form
    }
    return render(request,'signup.html',context)

@login_required(login_url='login')
def user_profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=account)
    
    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('home')
        
        form = UserProfileUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated sucessfully")
            return redirect('user_profile')
        else:
            print(form.errors)

    context = {
        "account": account,
        "form": form
    }
    return render (request,'user_profile.html',context)

@login_required
def change_profile_picture(request):
    if request.method == "POST":
        
        form = ProfilePictureUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = request.FILES['profile_image']
            user = get_object_or_404(User, pk=request.user.pk)
            
            if request.user.pk != user.pk:
                return redirect('home')

            user.profile_dp = image
            user.save()
            messages.success(request, "Profile image updated successfully")

        else:
            print(form.errors)

    return redirect('user_profile')


def view_profile(request,username):
    account = get_object_or_404(User, username = username)
    following = False
    muted = None

    if request.user.is_authenticated:
        
        if request.user.id == account.id:
            return redirect('user_profile')
        followers = account.followers.filter(
            followed_by__id = request.user.id
        )
        
        if followers.exists():
            following = True
            messages.success(request, "You have started following  " + account.username)

    
    if following:
        queryset = followers.first()
        if queryset.muted:
            muted = True
        else:
            muted = False
    context = {
        "account":account,
        "following": following,
        "muted": muted
    }
    return render(request,'view_profile.html',context)

#Follow/Unfolow
@login_required(login_url = "login")
def follow_or_unfollow_user(request, user_id):
    followed = get_object_or_404(User, id=user_id)
    followed_by = get_object_or_404(User, id=request.user.id)

    follow, created = Follow.objects.get_or_create(
        followed=followed,
        followed_by=followed_by
    )

    if created:
        followed.followers.add(follow)

    else:
        followed.followers.remove(follow)
        
        follow.delete()
        messages.success(request, "Profile is unfollowed!  ")

    return redirect("view_profile", username=followed.username)

#Notifications Show
@login_required(login_url="login")
def user_notifications(request):

    notifications = Notifications.objects.filter(
        user = request.user,
        is_seen = False
    )

    for notify in notifications:
        notify.is_seen = True
        notify.save()
    return render(request,'notifications.html')