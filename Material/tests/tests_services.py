from decimal import Decimal

from django.core import exceptions

from rest_framework.test import APITestCase,APIRequestFactory

from Material.models import Material,MaterialQuantity,MaterialStock
from Store.models import Store,Product
from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Material.services.material_services import (list_material_service, create_material_service, 
update_material_service, delete_material_service, list_material_stock_service, 
create_material_stock_service, update_max_capacity_service, delete_material_stock_service, 
list_material_quantity_service, create_material_quantity_service, update_material_quantity_service, 
delete_material_quantity_service)


class TestMaterialServices(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()
        
    """
    Material Services Test
    """
    def test_list_material_success(self):
        response = list_material_service()
        expected_result_array = [
            {"material_id":1,"price":Decimal("5.00"),"name":"wood"},
            {"material_id":2,"price":Decimal("1.30"),"name":"plastic"},
            {"material_id":3,"price":Decimal("10.50"),"name":"steel"}
        ]
        i=0
        for r in response:
            self.assertEqual(r.material_id,expected_result_array[i]["material_id"])
            self.assertEqual(r.price,expected_result_array[i]["price"])
            self.assertEqual(r.name,expected_result_array[i]["name"])
            i+=1

    def test_create_material(self):
        request = self.factory.post('/')
        request.data = {"name":"silver","price":150.00}
        response = create_material_service(request)
        self.assertEqual(response.name,"silver")
        self.assertEqual(response.price, Decimal("150.00"))

    def test_update_material(self):
        request = self.factory.put('/')
        request.data = {"name":"wood","price":4.00}
        response = update_material_service(request,material_uuid=Material.objects.get(material_id=1).uuid)
        self.assertEqual(response.name,"wood")
        self.assertEqual(response.price, Decimal("4.00"))
    
    def test_update_material_fail(self):
        request = self.factory.put('/')
        request.data = {"name":"wood","price":4.00}
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            self.assertFalse(update_material_service(request,material_uuid=Material.objects.get(material_id=4).uuid))

    def test_delete_material(self):
        self.assertTrue(delete_material_service(material_uuid=Material.objects.get(material_id=1).uuid))
    
    def test_delete_material_fail(self):
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            self.assertFalse(delete_material_service(material_uuid=Material.objects.get(material_id=4).uuid))

    """
    Material Stock Services Test
    """

    def test_list_material_stock_service_success(self):
        request = self.factory.get("/",)
        request.user = self.user
        response = list_material_stock_service(request,store_uuid = Store.objects.get(store_id=1).uuid)
        expected_result_array = [
            {
                "max_capacity":200,
                "current_capacity":104,
                "material":{"material_id":1,"price":Decimal("5.00"),"name":"wood"}
            },
            {
                "max_capacity":100,
                "current_capacity":45,
                "material":{"material_id":3,"price":Decimal("10.50"),"name":"steel"}
            }
        ]
        i=0
        for r in response:
            self.assertEqual(r.max_capacity, expected_result_array[i]["max_capacity"])
            self.assertEqual(r.current_capacity, expected_result_array[i]["current_capacity"])
            self.assertEqual(r.material.price,expected_result_array[i]["material"]["price"])
            self.assertEqual(r.material.name,expected_result_array[i]["material"]["name"])
            i+=1

    def test_list_material_stock_service_user_id_2_success(self):
        request = self.factory.get("/",)
        request.user = self.user2
        response = list_material_stock_service(request,store_uuid = Store.objects.get(store_id=3).uuid)
        expected_result = {
                "max_capacity":230,
                "current_capacity":144,
                "material":{"material_id":2,"price":Decimal("1.30"),"name":"plastic"}
            }
        self.assertEqual(response[0].max_capacity, expected_result["max_capacity"])
        self.assertEqual(response[0].current_capacity, expected_result["current_capacity"])
        self.assertEqual(response[0].material.price,expected_result["material"]["price"])
        self.assertEqual(response[0].material.name,expected_result["material"]["name"])
           
    def test_list_material_stock_service_no_material_stock_fail(self):
        request = self.factory.get("/",)
        request.user = self.user
        self.assertFalse(list_material_stock_service(request,store_uuid = Store.objects.get(store_id=3).uuid))

    def test_list_material_stock_service_no_store_fail(self):
        request = self.factory.get("/",)
        request.user = self.user3
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            self.assertFalse(list_material_stock_service(request,store_uuid = Store.objects.get(store_id=4).uuid))

    def test_create_material_stock(self):
        request = self.factory.post("/")
        request.user = self.user2
        request.data={"current_capacity":200,"max_capacity":400}
        store_uuid = Store.objects.get(store_id=3).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        response  = create_material_stock_service(request,store_uuid=store_uuid,material_uuid=material_uuid)
        self.assertEqual(response.current_capacity,200)
        self.assertEqual(response.max_capacity,400)
    
    def test_create_material_stock_fail(self):
        request = self.factory.post("/")
        request.user = self.user3
        request.data={"current_capacity":200,"max_capacity":400}
        store_uuid = Store.objects.get(store_id=3).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        self.assertFalse( create_material_stock_service(request,store_uuid=store_uuid,material_uuid=material_uuid))

    def test_update_max_capacity(self):
        request = self.factory.put("/")
        request.user = self.user
        request.data={"max_capacity":400}
        store_uuid = Store.objects.get(store_id=1).uuid
        material_stock_uuid = MaterialStock.objects.get(id=1).uuid
        response = update_max_capacity_service(request,store_uuid=store_uuid,material_stock_uuid=material_stock_uuid)
        self.assertEqual(response.max_capacity,400)
    
    def test_update_max_capacity_fail(self):
        request = self.factory.put("/")
        request.user = self.user
        request.data={"max_capacity":400}
        store_uuid = Store.objects.get(store_id=3).uuid
        material_stock_uuid = MaterialStock.objects.get(id=1).uuid
        self.assertFalse(update_max_capacity_service(request,store_uuid=store_uuid,material_stock_uuid=material_stock_uuid))

    def test_delete_material_stock(self):
        request = self.factory.delete("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=1).uuid
        material_stock_uuid = MaterialStock.objects.get(id=1).uuid
        self.assertTrue(delete_material_stock_service(request,store_uuid=store_uuid,material_stock_uuid=material_stock_uuid))
        
    def test_delete_material_stock_fail(self):
        request = self.factory.delete("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=1).uuid
        material_stock_uuid = MaterialStock.objects.get(id=3).uuid
        self.assertFalse(delete_material_stock_service(request,store_uuid=store_uuid,material_stock_uuid=material_stock_uuid))
        

    """
    Material Quantity Services Test
    """
    
    def test_create_material_quantity(self):
        request = self.factory.put("/")
        request.user = self.user2
        request.data={"quantity":2}
        store_uuid = Store.objects.get(store_id=3).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        response = create_material_quantity_service(request,store_uuid=store_uuid,material_uuid=material_uuid,product_uuid=product_uuid)
        self.assertEqual(response.quantity,2)
    
    def test_create_material_quantity_fail(self):
        request = self.factory.put("/")
        request.user = self.user2
        request.data={"quantity":2}
        store_uuid = Store.objects.get(store_id=1).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        self.assertFalse(create_material_quantity_service(request, store_uuid=store_uuid, material_uuid=material_uuid, product_uuid=product_uuid))

    def test_update_material_quantity(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data={"quantity":6}
        store_uuid = Store.objects.get(store_id=1).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        material_quantity_uuid = MaterialQuantity.objects.get(id = 1).uuid
        response = update_material_quantity_service(request, store_uuid=store_uuid, material_uuid=material_uuid, product_uuid=product_uuid, material_quantity_uuid=material_quantity_uuid)
        self.assertEqual(response.quantity,6)
    
    def test_update_material_quantity_fail(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data={"quantity":6}
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            store_uuid = Store.objects.get(store_id=1).uuid
            material_uuid = Material.objects.get(material_id=1).uuid
            product_uuid = Product.objects.get(id=1).uuid
            material_quantity_uuid = MaterialQuantity.objects.get(id=3).uuid
            self.assertFalse(update_material_quantity_service(request, store_uuid=store_uuid, material_uuid=material_uuid, product_uuid=product_uuid, material_quantity_uuid=material_quantity_uuid))
        

    def test_list_material_quantity(self):
        request = self.factory.get("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        response = list_material_quantity_service(request,store_uuid=store_uuid,product_uuid=product_uuid)
        self.assertEqual(len(response),2)

    def test_list_material_quantity_fail(self):
        request = self.factory.get("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=3).uuid
        product_uuid = Product.objects.get(id=1).uuid
        self.assertFalse(list_material_quantity_service(request,store_uuid=store_uuid,product_uuid=product_uuid))

    def test_delete_material_quantity(self):
        request = self.factory.delete("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=1).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        material_quantity_uuid = MaterialQuantity.objects.get(id = 1).uuid
        self.assertTrue(delete_material_quantity_service(request, store_uuid=store_uuid, material_uuid=material_uuid, product_uuid=product_uuid, material_quantity_uuid=material_quantity_uuid))
    
    def test_delete_material_quantity_fail(self):
        request = self.factory.delete("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=3).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        material_quantity_uuid = MaterialQuantity.objects.get(id = 1).uuid
        self.assertFalse(delete_material_quantity_service(request, store_uuid=store_uuid, material_uuid=material_uuid, product_uuid=product_uuid, material_quantity_uuid=material_quantity_uuid))
        