from decimal import Decimal

from rest_framework.test import APITestCase,APIRequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Store.services.store_services import get_store_service,get_stores_service,list_product_service,update_store_name_service,delete_store_service,update_product_name_service,delete_product_service
from Store.models import Product

class TestStoreServices(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()

    def test_get_stores_success(self):
        user = User.objects.get(id=1)
        get_stores_service(user)

    def test_get_stores_fail(self):
        user = User.objects.get(id=3)
        self.assertFalse(get_stores_service(user))
    
    def test_get_store_with_id_success(self):
        user =  User.objects.get(id=1)
        get_store_service(user,1)
    
    def test_get_store_with_id_fail(self):
        user = User.objects.get(id=2)
        self.assertFalse(get_store_service(user,1))
    
    def test_get_store_no_store_fail(self):
        user = User.objects.get(id=3)
        self.assertFalse(get_store_service(user,1))

    """
    POST Store test here
    """

    def test_update_store_name(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data = {"store_name":"Test_Store_Name"}
        response = update_store_name_service(request,store_id = 1)
        self.assertEqual(response.store_name,"Test_Store_Name")
    
    def test_update_store_name_fail(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data = {"store_name":"Test_Store_Name"}
        self.assertFalse(update_store_name_service(request,store_id = 3))

    def test_delete_store(self):
        request = self.factory.delete("/")
        request.user = self.user
        self.assertTrue(delete_store_service(request=request, store_id=1))
    
    def test_delete_store_fail(self):
        request = self.factory.delete("/")
        request.user = self.user
        self.assertFalse(delete_store_service(request=request, store_id=3))

    def test_list_product_service_success(self):
        request = self.factory.get("/",)
        request.user = self.user
        response = list_product_service(request, store_id = 1)
        if response:
            i=1
            for r in response:
                #the product id return in response should be 1 and 2. Refer to initialProductSetUp()
                self.assertEqual(r.name,Product.objects.get(id=i).name)
                i+=1
    
    def test_list_product_service_no_store_fail(self):
        request = self.factory.get("/",)
        request.user = self.user
        self.assertFalse(list_product_service(request,store_id = 3))

    def test_list_product_service_no_product_fail(self):
        request = self.factory.get("/",)
        request.user = self.user
        self.assertFalse(list_product_service(request,store_id = 2))

    """
    POST product test here
    """

    def test_update_product_name(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data={"name":"Test_Chair"}
        response = update_product_name_service(request,store_id=1,product_id=1)
        self.assertEqual(response.name,"Test_Chair")

    def test_update_product_name_fail(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data={"name":"Test_Chair"}
        self.assertFalse(update_product_name_service(request,store_id=1,product_id=3))
        
    def test_delete_product(self):
        request = self.factory.delete("/")
        request.user = self.user
        self.assertTrue(delete_product_service(request,store_id=1,product_id=1))

    def test_delete_product_fail(self):
        request = self.factory.delete("/")
        request.user = self.user
        self.assertFalse(delete_product_service(request,store_id=1,product_id=3))