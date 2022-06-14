from django.shortcuts import render

#LogIn
def login_user(request):
    return render(request,'login.html')
def signup_user(request):
    return render(request,'signup.html')