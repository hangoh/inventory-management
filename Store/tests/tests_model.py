import unittest

from django.core import exceptions
from django.contrib.auth.models import User

from .factories import StoreFactory,ProductFactory

from Material.models import Product

"""
Test in This Sequence
1. python manage.py test Account.tests.tests_model
2. python manage.py test Store.tests.tests_model
3. python manage.py test Material.tests.tests_model                  
"""

class TestProductFactory(unittest.TestCase):
    def test_product_creation(self):
        product = ProductFactory.create(name="chair" )
        # product of id=1 should have name="chair"
        self.assertEqual(product.id,1)
        self.assertEqual(product.name,"chair")
    
    def test_product_no_name_error(self):
        with self.assertRaises(exceptions.ValidationError):
            instance =  ProductFactory.build()
            instance.full_clean()


class TestStoreFactory(unittest.TestCase):
    def test_store_creation(self):
        self.user = User.objects.get(id=1)
        self.all_products =[]
        #will return as query
        self.products = Product.objects.all()
        #append all objects into array
        for p in self.products:
            self.all_products.append(p)
        store = StoreFactory.create(store_name = "Just_A_Store", user = self.user , products=self.all_products)
        product = ProductFactory.create(name="table" )
        self.assertEqual(product.id,2)
        self.assertEqual(product.name,"table")
        store.products.add(product)
        self.assertEqual(store.products.count(),2)
        self.assertEqual(store.store_name,"Just_A_Store")

    def test_store_no_name_error(self):
        with self.assertRaises(exceptions.ValidationError):
            instance = StoreFactory.build()
            instance.full_clean()