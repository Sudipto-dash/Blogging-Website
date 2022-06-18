import imp
from pydoc import pager
from django.db.models import Q
from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render
from matplotlib.style import context
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from platformdirs import user_cache_dir
from .form import TextForm
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
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
    liked_by = request.user in blog.likes.all() #checks user if liked or not
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
        "form": form,
        "liked_by":liked_by
    }
    return render(request,'blog_details.html',context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def like_blog(request, pk):
    context = {}
    blog = get_object_or_404(Blog, pk=pk)
    
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] = False
        context['like_count'] = blog.likes.all().count()
        
    else:
        blog.likes.add(request.user)
        context['liked'] = True
        context['like_count'] = blog.likes.all().count()

    return JsonResponse(context, safe=False)

def search_blogs(request): #Searching
    search_key = request.GET.get('search', None)
    recent_blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    
    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_key) |
            Q(category__title__icontains=search_key) |
            Q(user__username__icontains=search_key) |
            Q(tags__title__icontains=search_key)
        ).distinct()

        context = {
            "blogs": blogs,
            "recent_blogs": recent_blogs,
            "tags": tags,
            "search_key": search_key
        }

        return render(request, 'search_result.html', context)

    else:
        return redirect('home')
    