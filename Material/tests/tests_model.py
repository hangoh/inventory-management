from decimal import Decimal

from django.db import IntegrityError
from Material.models import Material, Material_Quantity,Material_Stock,Product
import factory
from factory.django import DjangoModelFactory
import unittest
from Account.tests.tests_model import UserModelFactory
from Account.models import User
from Material.models import Store
from django.core import exceptions

# Create your tests here.
class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
    
    # The Id will always be the total object count of Product + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:Product.objects.all().count()+1)
    name = ""


class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store
    
    # The Id will always be the total object count of Product + 1, if the Id is not provided
    store_id = factory.LazyAttribute(lambda n:Store.objects.all().count()+1)
    store_name = ""
    user = factory.SubFactory(UserModelFactory)


    #Required for many to many relationship field
    @factory.post_generation
    def products(self,create,extrated,**kwargs):
        if not create:
            return
        if extrated:
            for product in extrated:
                self.products.add(product)

class MaterialFactory(DjangoModelFactory):
    class Meta:
        model = Material

    # The Id will always be the total object count of Material + 1, if the Id is not provided
    material_id = factory.LazyAttribute(lambda n:Material.objects.all().count()+1)
    price = 2.00
    name = ""

class MaterialQuantityFactory(DjangoModelFactory):
    class Meta:
        model = Material_Quantity

    # The Id will always be the total object count of Material Quantity + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:Material_Quantity.objects.all().count()+1)
    quantity = 10
    product = factory.SubFactory(ProductFactory)
    ingredient = factory.SubFactory(MaterialFactory)

class MaterialStockFactory(DjangoModelFactory):
    class Meta:
        model = Material_Stock

    # The Id will always be the total object count of Material Stock + 1, if the Id is not provided
    id = factory.LazyAttribute(lambda n:Material_Stock.objects.all().count()+1)
    material = factory.SubFactory(MaterialFactory)
    store = factory.SubFactory(StoreFactory)
    max_capacity = 100
    current_capacity = 50


"""
//////////////////////
Test Factories Section
//////////////////////
"""

class TestMaterialFactory(unittest.TestCase):
    def test_Material_creation(self):
        material = MaterialFactory.create(material_id=1,price=2.30,name='plastic')
        self.assertEqual(material.material_id, 1)
        self.assertEqual(material.price,2.30)
        self.assertEqual(material.name,"plastic")
        material = MaterialFactory.create(price=2.00,name="steel")
        self.assertEqual(material.material_id, 2)
        self.assertEqual(material.price,2.00)
        self.assertEqual(material.name,"steel")

    def test_material_name_not_unique_error(self):
        with self.assertRaises(IntegrityError):
            instance = MaterialFactory.create(material_id=4,price=2.00,name='plastic')
            instance.full_clean()
    
    def test_material_no_name_error(self):
        with self.assertRaises(exceptions.ValidationError):
            instance = MaterialFactory.build(material_id=5,price=2)
            instance.full_clean()

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
        for p in self. products:
            self.all_products.append(p)
        store = StoreFactory.create(store_name = "Just_A_Store", user = self.user , products=self.all_products)
        self.assertEqual(store.products.count(),1)
        self.assertEqual(store.store_name,"Just_A_Store")

    def test_store_no_name_error(self):
        with self.assertRaises(exceptions.ValidationError):
            instance = StoreFactory.build()
            instance.full_clean()



