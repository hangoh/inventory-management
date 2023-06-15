from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory,APITestCase,force_authenticate
from rest_framework import status

from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Store.views import ProductView,StoreView
from Store.models import Product,Store


class TestMaterialView(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()

    """
    Starting Section for StoreView
    """
    def test_getStores_success(self):
        url=reverse("liststores")
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = StoreView.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        i=1
        for data in response.data:
            store = Store.objects.get(store_id=i)
            self.assertEqual(data["store_id"],store.store_id )
            self.assertEqual(data["store_name"], store.store_name)
            i+=1

    def test_getStores_no_store_fail(self):
        url=reverse("liststores")
        user = User.objects.get(id=3)
        request = self.factory.get(url)
        view = StoreView.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_getStores_unauthorized_fail(self):
        url=reverse("liststores")
        request = self.factory.get(url)
        view = StoreView.as_view({"get":"retrieve"})
        force_authenticate(request)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_getStore_success(self):
        url=reverse("store",kwargs={"store_id":1})
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = StoreView.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        response = view(request,store_id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_id"], 1)
        self.assertEqual(response.data["store_name"], "UncleBen'S")

    def test_getStore_store_not_found_fail(self):
        url=reverse("store",kwargs={"store_id":3})
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = StoreView.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        response = view(request,store_id=3)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_getStore_store_no_store_fail(self):
        url=reverse("store",kwargs={"store_id":3})
        user = User.objects.get(id=3)
        request = self.factory.get(url)
        view = StoreView.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        response = view(request,store_id=3)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_getStore_store_unauthorized_fail(self):
        url=reverse("store",kwargs={"store_id":3})
        request = self.factory.get(url)
        view = StoreView.as_view({"get":"retrieve"})
        force_authenticate(request)
        response = view(request,store_id=3)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_store(self):
        url = reverse("store",kwargs={"store_id":1})
        request = self.factory.put(url, data={"store_name":"test_store_name"})
        user = User.objects.get(id=1)
        view = StoreView.as_view({"put":"update"})
        force_authenticate(request,user=user)
        response = view(request,store_id =1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_name"], "test_store_name")
    
    def test_update_store_fail(self):
        url = reverse("store",kwargs={"store_id":4})
        request = self.factory.put(url, data={"store_name":"test_store_name"})
        user = User.objects.get(id=1)
        view = StoreView.as_view({"put":"update"})
        force_authenticate(request,user=user)
        response = view(request,store_id =4)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy_store(self):
        url = reverse("store",kwargs={"store_id":1})
        request = self.factory.delete(url)
        user = User.objects.get(id=1)
        view = StoreView.as_view({"delete":"destroy"})
        force_authenticate(request,user=user)
        response = view(request,store_id =1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_destroy_store_fail(self):
        url = reverse("store",kwargs={"store_id":1})
        request = self.factory.delete(url)
        user = User.objects.get(id=1)
        view = StoreView.as_view({"delete":"destroy"})
        force_authenticate(request,user=user)
        response = view(request,store_id = 3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_store(self):
        url = reverse("liststores")
        request = self.factory.post(url, data={"store_name":"Test_Name"})
        view = StoreView.as_view({"post":"create"})
        force_authenticate(request,user = User.objects.get(id=1))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_name"], "Test_Name")
    
    def test_create_store_fail(self):
        url = reverse("liststores")
        request = self.factory.post(url, data={"store_name":"UncleBen'S"})
        view = StoreView.as_view({"post":"create"})
        force_authenticate(request,user = User.objects.get(id=1))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Ending Section for StoreView
    """

    """
    Starting Section for ProductView
    """
    
    def test_list_product_view_success(self):
        url = reverse("listproducts",kwargs={"store_id":1})
        user = User.objects.get(id=1)
        view = ProductView.as_view({"get":"retrieve"})
        request = self.factory.get(url)
        force_authenticate(request,user=user)
        response = view(request,store_id=1)
        i=1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for r in response.data:
            self.assertEqual(r["name"],Product.objects.get(id=i).name)
            self.assertEqual(r["id"],Product.objects.get(id=i).id)
            i+=1
    
    def test_list_product_view_fail(self):
        url = reverse("listproducts",kwargs={"store_id":2})
        user = User.objects.get(id=1)
        view = ProductView.as_view({"get":"retrieve"})
        request = self.factory.get(url)
        force_authenticate(request,user=user)
        response = view(request,store_id=2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"],"No Product")

    def test_update_product(self):
        url = reverse("product",kwargs={"store_id":1,"product_id":1})
        request = self.factory.put(url, data={"name":"test_Product_name"})
        user = User.objects.get(id=1)
        view = ProductView.as_view({"put":"update"})
        force_authenticate(request,user=user)
        response = view(request,store_id=1,product_id =1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test_Product_name")
    
    def test_update_product_fail(self):
        url = reverse("product",kwargs={"store_id":1,"product_id":3})
        request = self.factory.put(url, data={"name":"test_Product_name"})
        user = User.objects.get(id=1)
        view = ProductView.as_view({"put":"update"})
        force_authenticate(request,user=user)
        response = view(request,store_id=1,product_id =3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        url = reverse("product",kwargs={"store_id":1,"product_id":1})
        request = self.factory.delete(url)
        user = User.objects.get(id=1)
        view = ProductView.as_view({"delete":"destroy"})
        force_authenticate(request,user=user)
        response = view(request,store_id=1,product_id =1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_product_fail(self):
        url = reverse("product",kwargs={"store_id":1,"product_id":3})
        request = self.factory.delete(url)
        user = User.objects.get(id=1)
        view = ProductView.as_view({"delete":"destroy"})
        force_authenticate(request,user=user)
        response = view(request,store_id=1,product_id = 3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product(self):
        url = reverse("listproducts",kwargs={"store_id":1})
        user = User.objects.get(id=1)
        view = ProductView.as_view({"post":"create"})
        request = self.factory.post(url,data={"name":"Bed"})
        force_authenticate(request,user=user)
        response = view(request,store_id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"],"Bed")
    
    def test_create_product_fail(self):
        url = reverse("listproducts",kwargs={"store_id":1})
        user = User.objects.get(id=1)
        view = ProductView.as_view({"post":"create"})
        request = self.factory.post(url,data={"name":"Chair"})
        force_authenticate(request,user=user)
        response = view(request,store_id=3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
    """
    Ending Section for ProductView
    """