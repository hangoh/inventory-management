from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase,APIRequestFactory

from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Store.models import Product,Store
from Store.services.store_services import( get_store_service, get_stores_service, list_product_service,
update_store_name_service, delete_store_service, update_product_name_service, 
delete_product_service, create_store, create_product)


class TestStoreServices(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()

    """
    Store Services Test
    """

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
        store_uuid = Store.objects.get(store_id=1).uuid
        self.assertFalse(get_store_service(user,store_uuid))
    
    def test_get_store_no_store_fail(self):
        user = User.objects.get(id=3)
        store_uuid = Store.objects.get(store_id=1).uuid
        self.assertFalse(get_store_service(user,store_uuid))

    def test_create_store(self):
        user = User.objects.get(id=1)
        request = self.factory.post('/')
        request.data={"store_name":"Testing_store_name"}
        request.user = user
        response = create_store(request)
        self.assertEqual(response.store_name,"Testing_store_name")

    def test_update_store_name(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data = {"store_name":"Test_Store_Name"}
        store_uuid = Store.objects.get(store_id=1).uuid
        response = update_store_name_service(request,store_uuid = store_uuid)
        self.assertEqual(response.store_name,"Test_Store_Name")
    
    def test_update_store_name_fail(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data = {"store_name":"Test_Store_Name"}
        store_uuid = Store.objects.get(store_id=3).uuid
        self.assertFalse(update_store_name_service(request,store_uuid = store_uuid))

    def test_delete_store(self):
        request = self.factory.delete("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=1).uuid
        self.assertTrue(delete_store_service(request=request, store_uuid=store_uuid))
    
    def test_delete_store_fail(self):
        request = self.factory.delete("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=3).uuid
        self.assertFalse(delete_store_service(request=request, store_uuid=store_uuid))

    """
    Product Services Test
    """

    def test_list_product_service_success(self):
        request = self.factory.get("/",)
        request.user = self.user
        store_uuid = Store.objects.get(store_id=1).uuid
        response = list_product_service(request, store_uuid=store_uuid)
        if response:
            i=1
            for r in response:
                #the product id return in response should be 1 and 2. Refer to initialProductSetUp()
                self.assertEqual(r.name,Product.objects.get(id=i).name)
                i+=1
    
    def test_list_product_service_no_store_fail(self):
        request = self.factory.get("/",)
        request.user = self.user
        store_uuid = Store.objects.get(store_id=3).uuid
        self.assertFalse(list_product_service(request,store_uuid=store_uuid))

    def test_list_product_service_no_product_fail(self):
        request = self.factory.get("/",)
        request.user = self.user
        store_uuid = Store.objects.get(store_id=2).uuid
        self.assertFalse(list_product_service(request,store_uuid=store_uuid))

    def test_create_product(self):
        user = User.objects.get(id=1)
        request = self.factory.post('/')
        request.user = user
        request.data={"name":"Bed"}
        store_uuid = Store.objects.get(store_id=1).uuid
        response = create_product(request,store_uuid=store_uuid)
        self.assertEqual(response.name,"Bed")
    
    def test_create_product_fail(self):
        user = User.objects.get(id=1)
        request = self.factory.post('/')
        request.user = user
        request.data={"name":"Bed"}
        store_uuid = Store.objects.get(store_id=3).uuid
        self.assertFalse(create_product(request,store_uuid=store_uuid))

    def test_update_product_name(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data={"name":"Test_Chair"}
        store_uuid = Store.objects.get(store_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        response = update_product_name_service(request,store_uuid=store_uuid,product_uuid=product_uuid)
        self.assertEqual(response.name,"Test_Chair")

    def test_update_product_name_fail(self):
        request = self.factory.post("/")
        request.user = self.user
        request.data={"name":"Test_Chair"}
        store_uuid = Store.objects.get(store_id=2).uuid
        product_uuid = Product.objects.get(id=2).uuid
        self.assertFalse(update_product_name_service(request,store_uuid=store_uuid,product_uuid=product_uuid))
        
    def test_delete_product(self):
        request = self.factory.delete("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        self.assertTrue(delete_product_service(request,store_uuid=store_uuid,product_uuid=product_uuid))

    def test_delete_product_fail(self):
        request = self.factory.delete("/")
        request.user = self.user
        store_uuid = Store.objects.get(store_id=2).uuid
        product_uuid = Product.objects.get(id=2).uuid
        self.assertFalse(delete_product_service(request,store_uuid=store_uuid,product_uuid=product_uuid))