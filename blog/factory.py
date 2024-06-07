import factory
from django.contrib.auth.models import User
from blog.models import Blog
from mysite.factory import UserFactoryExist, UserFactoryNewBlog


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog
    title = factory.Faker('text',max_nb_chars=100)
    description = factory.Faker('sentence',nb_words=10)
    level = factory.Faker('random_element',elements=('Beginner','Intermediate','Advanced'))
    videoID = factory.Faker('lexify',text='??????????')
    user_id = factory.SubFactory(UserFactoryExist)
    

class BlogFactoryNew(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog
    title = factory.Faker('text',max_nb_chars=100)
    description = factory.Faker('sentence',nb_words=10)
    level = factory.Faker('random_choices',elements=('Beginner','Intermediate','Advanced'))
    videoID = factory.Faker('lexify',text='??????????')
    user_id = factory.SubFactory(UserFactoryNewBlog)

