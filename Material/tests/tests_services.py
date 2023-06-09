from decimal import Decimal

from django.core import exceptions

from rest_framework.test import APITestCase,APIRequestFactory

from Material.models import Material,MaterialQuantity,MaterialStock
from Store.models import Store,Product
from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Material.services.material_services import ( list_material_stock_service, 
create_material_stock_service, list_material_quantity_service, create_material_quantity_service, 
check_for_restock, request_for_restock)


class TestMaterialServices(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()
        
    """
    Material Stock Services Test
    """

    def test_list_material_stock_service_success(self):
        request = self.factory.get("/",)
        request.user = self.user
        response = list_material_stock_service(request,store_uuid = Store.objects.get(store_id=1).store_uuid)
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
        response = list_material_stock_service(request,store_uuid = Store.objects.get(store_id=3).store_uuid)
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
        self.assertFalse(list_material_stock_service(request,store_uuid = Store.objects.get(store_id=3).store_uuid))

    def test_list_material_stock_service_no_store_fail(self):
        request = self.factory.get("/",)
        request.user = self.user3
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            self.assertFalse(list_material_stock_service(request,store_uuid = Store.objects.get(store_id=4).store_uuid))

    def test_create_material_stock(self):
        request = self.factory.post("/")
        request.user = self.user2
        request.data={"current_capacity":200,"max_capacity":400}
        store_uuid = Store.objects.get(store_id=3).store_uuid
        material_uuid = Material.objects.get(material_id=1).material_uuid
        response  = create_material_stock_service(request,store_uuid=store_uuid,material_uuid=material_uuid)
        self.assertEqual(response.current_capacity,200)
        self.assertEqual(response.max_capacity,400)
    
    def test_create_material_stock_fail(self):
        request = self.factory.post("/")
        request.user = self.user3
        request.data={"current_capacity":200,"max_capacity":400}
        store_uuid = Store.objects.get(store_id=3).store_uuid
        material_uuid = Material.objects.get(material_id=1).material_uuid
        self.assertFalse( create_material_stock_service(request,store_uuid=store_uuid,material_uuid=material_uuid))

    """
    Material Quantity Services Test
    """
    
    def test_create_material_quantity(self):
        request = self.factory.put("/")
        request.user = self.user2
        request.data={"quantity":2}
        store_uuid = Store.objects.get(store_id=3).store_uuid
        material_uuid = Material.objects.get(material_id=1).material_uuid
        product_uuid = Product.objects.get(id=1).product_uuid
        response = create_material_quantity_service(request,store_uuid=store_uuid,material_uuid=material_uuid,product_uuid=product_uuid)
        self.assertEqual(response.quantity,2)
    
    def test_create_material_quantity_fail(self):
        request = self.factory.put("/")
        request.user = self.user2
        request.data={"quantity":2}
        store_uuid = Store.objects.get(store_id=1).store_uuid
        material_uuid = Material.objects.get(material_id=1).material_uuid
        product_uuid = Product.objects.get(id=1).product_uuid
        self.assertFalse(create_material_quantity_service(request, store_uuid=store_uuid, material_uuid=material_uuid, product_uuid=product_uuid))


    def test_list_material_quantity(self):
        request = self.factory.get("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=1).store_uuid
        product_uuid = Product.objects.get(id=1).product_uuid
        response = list_material_quantity_service(request,store_uuid=store_uuid,product_uuid=product_uuid)
        self.assertEqual(len(response),2)

    def test_list_material_quantity_fail(self):
        request = self.factory.get("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=3).store_uuid
        product_uuid = Product.objects.get(id=1).product_uuid
        self.assertFalse(list_material_quantity_service(request,store_uuid=store_uuid,product_uuid=product_uuid))


  
    """
    restock services test
    """

    def test_check_for_restock(self):
        request = self.factory.get('/')
        request.user = self.user 
        material_stock_uuid = MaterialStock.objects.get(id = 1).material_stock_uuid
        response = check_for_restock(material_stock_uuid = material_stock_uuid)
        # expected_price = (200-104)*5.00 = 480
        self.assertEqual(response, 480.00)

    def test_check_for_restock_fail(self):
        request = self.factory.get('/')
        request.user = self.user 
        # provide a uuid that is not belong to material stock object 
        material_stock_uuid = Material.objects.get(material_id = 1).material_uuid
        response = check_for_restock(material_stock_uuid = material_stock_uuid)
        # expected response == None since an invalid uuid is provided
        self.assertEqual(response, None)

    def test_request_for_restock(self):
        request = self.factory.post('/')
        request.user = self.user 
        material_stock_uuid = MaterialStock.objects.get(id = 1).material_stock_uuid
        response = request_for_restock(material_stock_uuid = material_stock_uuid)
        # expected amount to restock = 200-104
        self.assertEqual(response, 96)

    def test_request_for_restock_fail(self):
        request = self.factory.post('/')
        request.user = self.user 
        # provide a uuid that is not belong to material stock object 
        material_stock_uuid = Material.objects.get(material_id = 1).material_uuid
        response = request_for_restock(material_stock_uuid = material_stock_uuid)
        # expected amount to restock == False since an invalid uuid is provided
        self.assertEqual(response, False)