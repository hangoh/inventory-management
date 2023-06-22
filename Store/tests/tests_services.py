from django.contrib.auth.models import User

from rest_framework.test import APITestCase,APIRequestFactory

from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Store.models import Product,Store
from Store.services.store_services import(get_store_service, get_stores_service, list_product_service,
 create_product_service, calculate_remaining_product_quantity_service,
product_sales_services)


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
        store_uuid = Store.objects.get(store_id=1).store_uuid
        self.assertFalse(get_store_service(user,store_uuid))
    
    def test_get_store_no_store_fail(self):
        user = User.objects.get(id=3)
        store_uuid = Store.objects.get(store_id=1).store_uuid
        self.assertFalse(get_store_service(user,store_uuid))

    """
    Product Services Test
    """

    def test_list_product_service_success(self):
        request = self.factory.get("/",)
        request.user = self.user
        store_uuid = Store.objects.get(store_id=1).store_uuid
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
        store_uuid = Store.objects.get(store_id=3).store_uuid
        self.assertFalse(list_product_service(request,store_uuid=store_uuid))

    def test_list_product_service_no_product_fail(self):
        request = self.factory.get("/",)
        request.user = self.user
        store_uuid = Store.objects.get(store_id=2).store_uuid
        self.assertFalse(list_product_service(request,store_uuid=store_uuid))

    def test_create_product_service(self):
        user = User.objects.get(id=1)
        request = self.factory.post('/')
        request.user = user
        request.data={"name":"Bed"}
        store_uuid = Store.objects.get(store_id=1).store_uuid
        response = create_product_service(request,store_uuid=store_uuid)
        self.assertEqual(response.name,"Bed")
    
    def test_create_product_service_fail(self):
        user = User.objects.get(id=1)
        request = self.factory.post('/')
        request.user = user
        request.data={"name":"Bed"}
        store_uuid = Store.objects.get(store_id=3).store_uuid
        self.assertFalse(create_product_service(request,store_uuid=store_uuid))

    """
    remaining product capacity services test
    """

    def test_calculate_remaining_product_capacity(self):
        request = self.factory.get("/")
        request.user = self.user
        material_quantity=[5,6]
        material_stock_current_capacity=[55,55]
        response = calculate_remaining_product_quantity_service(material_quantity=material_quantity,material_stock_current_capacity=material_stock_current_capacity)
        self.assertEqual(response,9)

    """
    Product sales service test
    """

    def test_product_sale_service(self):
        request = self.factory.post('/')
        request.user = self.user
        product = Product.objects.get(id = 1)
        request.data = {"products":[{"quantity":2,"uuid":product.product_uuid}]}
        response = product_sales_services(request, store_uuid = Store.objects.get(store_id = 1).store_uuid)
        self.assertEqual(response["sale"][0]["quantity"], 2)
        self.assertEqual(response["sale"][0]["product"], product.product_uuid)

    def test_product_sale_service_fail(self):
        request = self.factory.post('/')
        request.user = self.user
        product = Product.objects.get(id = 1)
        request.data = {"products":[{"quantity":2,"uuid":product.product_uuid}]}
        response = product_sales_services(request, store_uuid = Store.objects.get(store_id = 2).store_uuid)
        self.assertEqual(response["error"][0]["product"], product.product_uuid)
        self.assertEqual(response["error"][0]["error"], "Fail to Update Sale For This Product uuid {}".format(product.product_uuid))
        