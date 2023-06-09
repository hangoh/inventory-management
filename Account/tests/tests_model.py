
from django.db import IntegrityError
from Account.models import User
import unittest
import factory
from factory.django import DjangoModelFactory
from django.core import exceptions

class UserModelFactory(DjangoModelFactory):
    class Meta:
        model = User
        
    # The Id will always be the total object count of User + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:User.objects.all().count()+1)

class TestUserModel(unittest.TestCase):
    def test_User_model_creation(self):
        user_model = UserModelFactory.create(id=1,name="UncleBen")
        self.assertEqual(user_model.id, 1)
        self.assertEqual(user_model.name, "UncleBen")
        self.assertIsInstance(user_model,User)
    
    def test_user_no_username_error(self):
        with self.assertRaises(exceptions.ValidationError):   
            instance = UserModelFactory.build()
            instance.full_clean()

    
    def test_user_username_not_unique_error(self):
        with self.assertRaises(IntegrityError):
            UserModelFactory.create(name="UncleBen")
            


    
    
    
    