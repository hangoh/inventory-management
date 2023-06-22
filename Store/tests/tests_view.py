from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory,APITestCase,force_authenticate
from rest_framework import status

from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Store.views import ProductViewSet, StoreViewSet, ProductCapacityViewSet, SalesViewSet
from Store.models import Product, Store


class TestMaterialView(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()
        self.uuid = Store.objects.get(store_id=1).store_uuid

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
        store_uuid = Store.objects.get(store_id=1).store_uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_name"], "UncleBen'S")

    def test_get_store_store_not_found_fail(self):
        url=reverse("store",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=3).store_uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_store_store_no_store_fail(self):
        url=reverse("store",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=3)
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=3).store_uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_store_store_unauthorized_fail(self):
        url=reverse("store",kwargs={"store_uuid":self.uuid})
        request = self.factory.get(url)
        view = StoreViewSet.as_view({"get":"retrieve"})
        force_authenticate(request)
        store_uuid = Store.objects.get(store_id=3).store_uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
        store_uuid = Store.objects.get(store_id=1).store_uuid
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
        store_uuid = Store.objects.get(store_id=2).store_uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"],"No Product")

    def test_create_product(self):
        url = reverse("listproducts",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=1)
        view = ProductViewSet.as_view({"post":"create"})
        request = self.factory.post(url,data={"name":"Bed"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=1).store_uuid
        response = view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"],"Bed")
    
    def test_create_product_fail(self):
        url = reverse("listproducts",kwargs={"store_uuid":self.uuid})
        user = User.objects.get(id=1)
        view = ProductViewSet.as_view({"post":"create"})
        request = self.factory.post(url,data={"name":"Chair"})
        force_authenticate(request,user=user)
        store_uuid = Store.objects.get(store_id=3).store_uuid
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
        store_uuid = Store.objects.get(store_id = 2).store_uuid
        response  = view(request,store_uuid = store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """
    Product Sales View Test
    """
    
    def test_product_sales_view(self):
        url = reverse("productssales", kwargs={"store_uuid":self.uuid})
        product = Product.objects.get(id = 1)
        request = self.factory.post(url, data = {"products":[{"quantity":2,"uuid":product.product_uuid}]}, format = "json")
        view  = SalesViewSet.as_view({"post":"create"})
        force_authenticate(request, user = self.user)
        response = view(request, self.uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["sale"][0]["quantity"], 2)
        self.assertEqual(response.data["sale"][0]["product"], str(product.product_uuid))

    def test_product_sales_view_fail(self):
        url = reverse("productssales", kwargs={"store_uuid":self.uuid})
        product = Product.objects.get(id = 1)
        request = self.factory.post(url, data = {"products":[{"quantity":2,"uuid":product.product_uuid}]}, format = "json")
        view  = SalesViewSet.as_view({"post":"create"})
        force_authenticate(request, user = self.user)
        response = view(request, Store.objects.get(store_id = 2).store_uuid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"][0]["product"], str(product.product_uuid))
        self.assertEqual(response.data["error"][0]["error"], "Fail to Update Sale For This Product uuid {}".format(product.product_uuid))