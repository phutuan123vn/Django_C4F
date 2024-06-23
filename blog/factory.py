import factory
from django.contrib.auth.models import User
from blog.models import Blog,BlogComment,BlogLike
from mysite.factory import UserFactoryExist, UserFactoryNewBlog


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog
    title = factory.Faker('text',max_nb_chars=100)
    description = factory.Faker('sentence',nb_words=10)
    level = factory.Faker('random_choices',elements=('Beginner','Intermediate','Advanced'))
    videoID = factory.Faker('lexify',text='??????????')
    user_id = factory.SubFactory(UserFactoryExist)
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return Blog.objects.order_by('?').first()
        # return super().create(**kwargs)

class BlogFactoryNew(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog
    title = factory.Faker('text',max_nb_chars=100)
    description = factory.Faker('sentence',nb_words=10)
    level = factory.Faker('random_choices',elements=('Beginner','Intermediate','Advanced'))
    videoID = factory.Faker('lexify',text='??????????')
    user_id = factory.SubFactory(UserFactoryNewBlog)


class BlogCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogComment
        
    comment = factory.Faker('sentence',nb_words=20)
    blog_id = factory.SubFactory(BlogFactory)
    user_id = factory.SubFactory(UserFactoryExist)
    
    
class BlogLikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogLike
        
    blog_id = factory.SubFactory(BlogFactory)
    user_id = factory.SubFactory(UserFactoryExist)