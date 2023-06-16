import unittest
from decimal import Decimal

from django.core import exceptions
from django.db import IntegrityError

from .factories import MaterialFactory

from Store.models import Store,Product
from Material.models import MaterialStock,Material,MaterialQuantity
from Material.tests.factories import MaterialStockFactory,MaterialQuantityFactory

"""
Test in This Sequence
1. python manage.py test Account.tests.tests_model
2. python manage.py test Store.tests.tests_model
3. python manage.py test Material.tests.tests_model                  
"""


# Create your tests here.
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


class TestMaterialStockFactory(unittest.TestCase):
    def test_material_stock_creation(self):
        self.material_factory = Material.objects.get(material_id=1)
        self.store = Store.objects.get(store_id=1)
        material_stock = MaterialStockFactory.create(material = self.material_factory,store=self.store)
        self.assertEqual(material_stock.id,1)
        self.assertEqual(material_stock.max_capacity,100)
        self.assertEqual(material_stock.current_capacity,50)
        self.assertEqual(material_stock.material,self.material_factory)
        self.assertEqual(material_stock.store.store_id,self.store.store_id)
       
    #Test To Get The Material Stock Object with Id And Also 
    #Tends To Get The Material Objects Which Has A Relation Mapping Through
    #The Id Obtain From The Material Stock Object And Test If The Value Are 
    #As Expected

    def test_material_stock_get(self):
        m_s = MaterialStock.objects.get(id=1)
        m = Material.objects.get(material_id = m_s.material.material_id)
        # material of id=1 should have price = 2.30 and name = "plastic"
        self.assertEqual(m.price,Decimal("2.30"))
        self.assertEqual(m.name, "plastic") 
        # material_stock of id=1 should have current_capacity = 50,
        # max_capacity=100 and the material object in material 
        # should have material_id of 1
        self.assertEqual(m_s.id,1)
        self.assertEqual(m_s.current_capacity,50)
        self.assertEqual(m_s.max_capacity,100)
        self.assertEqual(m_s.material.material_id,1)

    def test_material_stock_current_capacity_not_positive_error(self):
        with self.assertRaises(exceptions.ValidationError):
            instance = MaterialStockFactory.build(max_capacity=100 ,current_capacity=-120)
            instance.full_clean()

    def test_material_stock_max_capacity_not_positive_error(self):
        with self.assertRaises(exceptions.ValidationError):
            instance = MaterialStockFactory.build(max_capacity=-100 ,current_capacity=20)
            instance.full_clean()


class TestMaterialQuantityFactory(unittest.TestCase):
    def test_material_quantity_creation(self):
        self.material_factory = Material.objects.get(material_id=1)
        self.product = Product.objects.get(id=1)
        material_quantity = MaterialQuantityFactory.create(quantity=5,ingredient = self.material_factory,product=self.product)
        self.assertEqual(material_quantity.id,1)
        self.assertEqual(material_quantity.quantity,5)
        self.assertEqual(material_quantity.ingredient,self.material_factory)
        self.assertEqual(material_quantity.product.name,self.product.name)

    #Test To Get The Material Quantity Object with Id And Also 
    #Tends To Get The Material Objects Which Has A Relation Mapping Through
    #The Id Obtain From The Material Quantity Object And Test If The Value Are 
    #As Expected

    def test_material_quantity_get(self):
        m_q = MaterialQuantity.objects.get(id=1)
        m = Material.objects.get(material_id = m_q.ingredient.material_id)
        p = Product.objects.get(id = m_q.product.id)
        # material of id=1 should have price = 2.3 and name = "plastic"
        self.assertEqual(m.price,Decimal("2.30"))
        self.assertEqual(m.name, "plastic") 
        # product of id=1 should name = "chair"
        self.assertEqual(p.name, "chair") 
        # material_quantity of id=1 should have quantity=55
        # and the material object in ingredient should have material_id of 1
        self.assertEqual(m_q.id,1)
        self.assertEqual(m_q.quantity,5)
        self.assertEqual(m_q.ingredient.material_id,m.material_id)
        self.assertEqual(m_q.product.name,p.name)

    def test_material_quantity_not_positive_error(self):
        with self.assertRaises(exceptions.ValidationError):
            instance = MaterialQuantityFactory.build(quantity=-55)
            instance.full_clean()