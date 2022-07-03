import imp
from django.db import models
from django.utils.text import slugify
from user_profile.models import User
from ckeditor.fields import RichTextField
from .slug import generate_slug

#Category
class Category(models.Model):
    title = models.CharField(max_length=150, unique=True) 
    slug = models.SlugField(null=True, blank=True) #Will filter through this 
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs): #Slug will auto generate, basis of Title
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        

#Tags
class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

#Blog
class Blog(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_blogs',
        on_delete=models.CASCADE #Delete on user deleted
    )
    category = models.ForeignKey(
        Category,
        related_name='category_blogs',
        on_delete=models.CASCADE #Delete on category deleted
    )

    tags = models.ManyToManyField(  #Multiple tags can be added
        Tag,
        related_name='tag_blogs',
        blank=True 
    )
    likes = models.ManyToManyField(
        User,
        related_name='user_likes',
        blank=True
    )
    title = models.CharField( #Blog Title
        max_length=250
    )
    slug = models.SlugField(null=True, blank=True)
    banner = models.ImageField(upload_to='blog_banners')
    description = RichTextField()
    created_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs): #Slug will auto generate, basis of Title
        updating = self.pk is not None
        
        if updating:
            self.slug = generate_slug(self,self.title,update=True)
            super().save(*args, **kwargs)
        else:
            self.slug = generate_slug(self, self.title)
            super().save(*args, **kwargs)


#Comments
class Comment(models.Model):
    user = models.ForeignKey( #User who commented
        User,
        related_name='user_comments',
        on_delete=models.CASCADE #if user delets then destroy
    )
    blog = models.ForeignKey( #On Which blog commented
        Blog,
        related_name='blog_comments',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text

#Reply
class Reply(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_replies',
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment,
        related_name='comment_replies',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text