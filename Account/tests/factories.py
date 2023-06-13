import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

class UserModelFactory(DjangoModelFactory):
    class Meta:
        model = User
        
    # The Id will always be the total object count of User + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:User.objects.all().count()+1)