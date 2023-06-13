from decimal import Decimal
from rest_framework.test import APITestCase,APIRequestFactory
from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Material.services.material_services import list_material_service,list_material_stock_service
from django.urls import reverse
from Material.models import Product

class TestMaterialServices(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()
        
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

    def test_list_material_stock_service_success(self):
        request = self.factory.get("/",)
        request.user = self.user
        response = list_material_stock_service(request,1)
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
            self.assertEqual(r.material.material_id,expected_result_array[i]["material"]["material_id"])
            self.assertEqual(r.material.price,expected_result_array[i]["material"]["price"])
            self.assertEqual(r.material.name,expected_result_array[i]["material"]["name"])
            i+=1

    def test_list_material_stock_service_user_id_2_success(self):
        request = self.factory.get("/",)
        request.user = self.user2
        response = list_material_stock_service(request,3)
        expected_result = {
                "max_capacity":230,
                "current_capacity":144,
                "material":{"material_id":2,"price":Decimal("1.30"),"name":"plastic"}
            }
        self.assertEqual(response[0].max_capacity, expected_result["max_capacity"])
        self.assertEqual(response[0].current_capacity, expected_result["current_capacity"])
        self.assertEqual(response[0].material.material_id,expected_result["material"]["material_id"])
        self.assertEqual(response[0].material.price,expected_result["material"]["price"])
        self.assertEqual(response[0].material.name,expected_result["material"]["name"])
           
    def test_list_material_stock_service_no_material_stock_fail(self):
        request = self.factory.get("/",)
        request.user = self.user
        self.assertFalse(list_material_stock_service(request,3))

    def test_list_material_stock_service_no_store_fail(self):
        request = self.factory.get("/",)
        request.user = self.user3
        self.assertFalse(list_material_stock_service(request,4))
        
       