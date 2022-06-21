import re
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from matplotlib.style import context
from django.views.decorators.cache import never_cache
from .forms import (
    userSignUpForm,
    loginForm
)
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

def user_profile(request):
    return render (request,'user_profile.html')