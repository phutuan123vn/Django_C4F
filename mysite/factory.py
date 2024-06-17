from django.contrib.auth.models import User
import factory


class UserFactoryNew(factory.Factory):
    class Meta:
        model = User
        
    username = factory.Faker("user_name")
    password = factory.django.Password('pw')

class UserFactoryNewBlog(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        
    username = factory.Faker("user_name")
    password = factory.django.Password('pw')

class UserFactoryExist(factory.Factory):
    class Meta:
        model = User


    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        existing_user = User.objects.order_by('?').first()
        return existing_user
    
    