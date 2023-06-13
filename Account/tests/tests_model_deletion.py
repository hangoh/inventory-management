import unittest
from django.contrib.auth.models import User
from Material.models import Store,Material_Stock

"""
Please proceed to this test after testing for
both test_model.py in Account and Material and 
test_model_2.py in Material 
"""

class TestUserDeletion(unittest.TestCase):
    def test_user_deletion_cascade(self):
        user = User.objects.get(id=1)
        user.delete()
        # User with id 1 will be remove (Of Course!)
        self.assertFalse(User.objects.filter(id=1).exists())
        # Store with store_id 1 is associate with User of id 1. 
        # Remove user should also remove store
        self.assertFalse(Store.objects.filter(store_id=1).exists())
        # Material stock with id 1 is associate with store of store_id 1. 
        # Removing store should also remove material stock
        self.assertFalse(Material_Stock.objects.filter(id=1).exists())