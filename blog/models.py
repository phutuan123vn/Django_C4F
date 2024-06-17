from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
# Create your models here.
class Blog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_user")
    title = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=100)
    videoID = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    

class BlogComment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_comment_user")
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_comment")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
    

class BlogLike(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_like_user")
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_like")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id.username
    



# class Publication(models.Model):
#     title = models.CharField(max_length=30)

#     class Meta:
#         ordering = ["title"]

#     def __str__(self):
#         return self.title


# class Article(models.Model):
#     headline = models.CharField(max_length=100)
#     publications = models.ManyToManyField(Publication)

#     class Meta:
#         ordering = ["headline"]

#     def __str__(self):
#         return self.headline