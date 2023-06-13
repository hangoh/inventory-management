import unittest
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core import exceptions

from Account.tests.factories import UserModelFactory

"""
Test in This Sequence
1. python manage.py test Account.tests.tests_model
2. python manage.py test Store.tests.tests_model
3. python manage.py test Material.tests.tests_model                   
"""

class TestUserModel(unittest.TestCase):
    def test_user_creation_success(self):
        user = User.objects.create_user(username="UncleBen",password="JustPassword")
        self.assertEqual(user.username,"UncleBen")

    def test_user_no_username_error(self):
        with self.assertRaises(exceptions.ValidationError):   
            instance = UserModelFactory.build(username="",password="JustPassword")
            instance.full_clean()

    
    def test_user_username_not_unique_error(self):
        with self.assertRaises(IntegrityError):
            UserModelFactory.create(username="UncleBen",password="JustPassword")
            


    
    
    
    