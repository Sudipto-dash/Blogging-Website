import imp
from pydoc import pager
from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render
from matplotlib.style import context
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from platformdirs import user_cache_dir
from .form import TextForm
from django.contrib.auth.decorators import login_required
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

def category_blogs(request,slug):
    category = get_object_or_404(Category,slug=slug)
    tags = Tag.objects.order_by('-created_date')[:5] #Showing 5 tags
    queryset = category.category_blogs.all()
    all_blog =Blog.objects.order_by('-created_date')[:5]
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
        "all_blog": all_blog
    }
    return render(request,'category_blogs.html',context)

def tag_blogs(request,slug):
    tag = get_object_or_404(Tag,slug=slug)
    tags = Tag.objects.order_by('-created_date')[:5] #Showing 5 tags
    queryset = tag.tag_blogs.all()
    all_blog =Blog.objects.order_by('-created_date')[:5]
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
        "all_blog": all_blog
    }
    return render(request,'tag_blogs.html',context)

def blog_details(request,slug):
    form = TextForm()
    blog = get_object_or_404(Blog,slug=slug)
    category = Category.objects.get(id = blog.category.id)
    tags = Tag.objects.order_by('-created_date')[:5]
    related_blogs = category.category_blogs.all()
    if request.method == "POST" and request.user.is_authenticated: #for commenting user authentication
        form = TextForm(request.POST) 
        if form.is_valid(): 
            Comment.objects.create(
                user = request.user,
                blog = blog,
                text = form.cleaned_data.get('text')
            )
            return redirect ('blog_details',slug=slug)

    context = {
        "blog": blog,
        "related_blogs":related_blogs,
        "tags":tags,
        "form": form
    }
    return render(request,'blog_details.html',context)

@login_required(login_url='/')
def add_reply(request, blog_id, comment_id): #For Reply comment
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('text')
            )
    return redirect('blog_details', slug=blog.slug)