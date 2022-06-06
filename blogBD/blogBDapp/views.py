import imp
from pydoc import pager
from django.shortcuts import redirect, render
from matplotlib.style import context
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator

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
    queryset = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2) #no. of blogs showing
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect("blogs")
    context = {
        "blogs": blogs,
        "tags": tags,
        "paginator":paginator
    }
    return render(request,'blogs.html',context)