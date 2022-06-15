from django.shortcuts import redirect


def not_logged_in_required(view_function):
    def wrapper(request, *args, **kwarsg):
        if request.user.is_authenticated: #Checks user authentications
            return redirect('home')
        else:
            return view_function(request, *args, **kwarsg) #returns to the view function
 
    return wrapper