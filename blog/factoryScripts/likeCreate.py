from blog.factory import BlogLikeFactory, BlogFactory
from mysite.factory import UserFactoryExist
from blog.models import BlogLike
import random

users = UserFactoryExist.create_batch(10)
blogs = BlogFactory.create_batch(10)

for user in  users:
    random.shuffle(blogs)
    for blog in blogs:
        if not BlogLike.objects.filter(blog_id=blog,user_id=user).exists():
            BlogLikeFactory.create(blog_id=blog,user_id=user)
