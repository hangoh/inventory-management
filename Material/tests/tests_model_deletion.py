import unittest
from Material.models import Product,MaterialQuantity,Material

"""
Please proceed to this test after testing for
both test_model.py in Account and Material and
test_model_2.py in Material 
"""

class TestProductDeletion(unittest.TestCase):
    def test_product_deletion(self):
        product=Product.objects.get(id=1)
        product.delete()
        # Product with id 1 will be remove (Of Course!)
        self.assertFalse(Product.objects.filter(id=1).exists())
        # Product with id 1 is associate with Material_Quantity id 1. 
        # Removing Product should also remove Material_Quantity
        self.assertFalse(MaterialQuantity.objects.filter(id=1).exists())
    

    def test_material_deletion(self):
        Material.objects.all().delete()
        # Material with id 1 will be remove (Of Course!)
        self.assertFalse(Material.objects.filter(material_id=1).exists())
        # Material with material_id 1 is associate with Material_Quantity id 1. 
        # Removing Material should also remove Material_Quantity
