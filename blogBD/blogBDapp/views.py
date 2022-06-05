from django.shortcuts import render
from matplotlib.style import context

from .models import (
    Blog,
    Category,
    Reply,
    Tag,
    Comment
) #importing models

def home(request):
    blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    context = {
        "blogs": blogs,
        "tags": tags
    }
    return render(request,'home.html',context)
def blogs(request):
    return render(request,'blogs.html')