from uuid import uuid4

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory,APITestCase,force_authenticate
from rest_framework import status

from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Store.views import ProductViewSet,StoreViewSet,ProductCapacityViewSet
from Store.models import Product,Store


class TestMaterialView(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()
        self.uuid = Store.objects.get(store_id=1).uuid

    """
    Starting Section for StoreViewSet
    """
    def test_get_stores_success(self):
        url=reverse("liststores")
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        i=1
        for data in response.data:
            store = Store.objects.get(store_id=i)
            self.assertEqual(data["store_name"], store.store_name)
            i+=1

    def test_get_stores_no_store_fail(self):
        url=reverse("liststores")
        user = User.objects.get(id=3)
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_stores_unauthorized_fail(self):
        url=reverse("liststores")
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_store_success(self):
        url=reverse("store",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=1).uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_name"], "UncleBen'S")

    def test_get_store_store_not_found_fail(self):
        url=reverse("store",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=3).uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_store_store_no_store_fail(self):
        url=reverse("store",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=3)
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=3).uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_store_store_unauthorized_fail(self):
        url=reverse("store",kwargs={"store_uuid":self.uuid})
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request)
        store_uuid = Store.objects.get(store_id=3).uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_store(self):
        url = reverse("store",kwargs={"store_uuid":self.uuid})
        request = self.factory.put(url, data={"store_name":"test_store_name"})
        user = User.objects.get(id=1)
        view = StoreViewSet.as_view({"put":"update"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=1).uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_name"], "test_store_name")
    
    def test_update_store_fail(self):
        url = reverse("store",kwargs={"store_uuid":self.uuid})
        request = self.factory.put(url, data={"store_name":"test_store_name"})
        user = User.objects.get(id=1)
        view = StoreViewSet.as_view({"put":"update"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=3).uuid
        response = view(request,store_uuid =store_uuid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy_store(self):
        url = reverse("store",kwargs={"store_uuid":self.uuid})
        request = self.factory.delete(url)
        user = User.objects.get(id=1)
        view = StoreViewSet.as_view({"delete":"destroy"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=1).uuid
        response = view(request,store_uuid =store_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_destroy_store_fail(self):
        url = reverse("store",kwargs={"store_uuid":self.uuid})
        request = self.factory.delete(url)
        user = User.objects.get(id=1)
        view = StoreViewSet.as_view({"delete":"destroy"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=3).uuid
        response = view(request,store_uuid = store_uuid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_store(self):
        url = reverse("liststores")
        request = self.factory.post(url, data={"store_name":"Test_Name"})
        view = StoreViewSet.as_view({"post":"create"})
        force_authenticate(request,user = User.objects.get(id=1))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_name"], "Test_Name")
    
    def test_create_store_fail(self):
        url = reverse("liststores")
        request = self.factory.post(url, data={"store_name":"UncleBen'S"})
        view = StoreViewSet.as_view({"post":"create"})
        force_authenticate(request,user = User.objects.get(id=1))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Ending Section for StoreViewSet
    """

    """
    Starting Section for ProductViewSet
    """
    
    def test_list_product_view_success(self):
        url = reverse("listproducts",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=1)
        view = ProductViewSet.as_view({"get":"retrieve"})
        request = self.factory.get(url)
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=1).uuid
        response = view(request,store_uuid=store_uuid)
        i=1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for r in response.data:
            self.assertEqual(r["name"],Product.objects.get(id=i).name)
            i+=1
    
    def test_list_product_view_fail(self):
        url = reverse("listproducts",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=1)
        view = ProductViewSet.as_view({"get":"retrieve"})
        request = self.factory.get(url)
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=2).uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"],"No Product")

    def test_update_product(self):
        url = reverse("product",kwargs={"store_uuid":self.uuid,"product_uuid":self.uuid})
        request = self.factory.put(url, data={"name":"test_Product_name"})
        user = User.objects.get(id=1)
        view = ProductViewSet.as_view({"put":"update"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        response = view(request,store_uuid=store_uuid,product_uuid =product_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test_Product_name")
    
    def test_update_product_fail(self):
        url = reverse("product",kwargs={"store_uuid":self.uuid,"product_uuid":self.uuid})
        request = self.factory.put(url, data={"name":"test_Product_name"})
        user = User.objects.get(id=2)
        view = ProductViewSet.as_view({"put":"update"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=1).uuid
        product_uuid = Product.objects.get(id=2).uuid
        response = view(request,store_uuid=store_uuid,product_uuid =product_uuid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        url = reverse("product",kwargs={"store_uuid":self.uuid,"product_uuid":self.uuid})
        request = self.factory.delete(url)
        user = User.objects.get(id=1)
        view = ProductViewSet.as_view({"delete":"destroy"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        response = view(request,store_uuid=store_uuid,product_uuid =product_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_product_fail(self):
        url = reverse("product",kwargs={"store_uuid":self.uuid,"product_uuid":self.uuid})
        request = self.factory.delete(url)
        user = User.objects.get(id=1)
        view = ProductViewSet.as_view({"delete":"destroy"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=2).uuid
        product_uuid = Product.objects.get(id=2).uuid
        response = view(request,store_uuid=store_uuid,product_uuid = product_uuid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product(self):
        url = reverse("listproducts",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=1)
        view = ProductViewSet.as_view({"post":"create"})
        request = self.factory.post(url,data={"name":"Bed"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=1).uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"],"Bed")
    
    def test_create_product_fail(self):
        url = reverse("listproducts",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=1)
        view = ProductViewSet.as_view({"post":"create"})
        request = self.factory.post(url,data={"name":"Chair"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=3).uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
    """
    Ending Section for ProductViewSet
    """

    """
    Remaining Product Capacity View 
    """

    def test_product_capacity_view(self):
        url = reverse("productscapacity", kwargs={"store_uuid":self.uuid})
        request = self.factory.get(url)
        view = ProductCapacityViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        response  = view(request,store_uuid=self.uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_query=[
            {"name":"Chair","quantity":20},
            {"name":"table","quantity":0},
        ]
        i=0
        for r in response.data:
            self.assertEqual(r["name"],expected_query[i]["name"])
            self.assertEqual(r["quantity"],expected_query[i]["quantity"])
            i+=1

    def test_product_capacity_view_fail(self):
        url = reverse("productscapacity", kwargs={"store_uuid":self.uuid})
        request = self.factory.get(url)
        view = ProductCapacityViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        store_uuid = Store.objects.get(store_id = 2).uuid
        response  = view(request,store_uuid = store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
       