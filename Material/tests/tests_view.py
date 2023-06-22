from django.urls import reverse
from django.core import exceptions

from rest_framework import status
from rest_framework.test import APIRequestFactory,APITestCase,force_authenticate

from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Material.views import  MaterialViewSet,MaterialStockViewSet,MaterialQuantityViewSet,MaterialRestockViewSet
from Material.models import Material,MaterialQuantity,MaterialStock
from Store.models import Store,Product


class TestMaterialViewSet(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()
        self.uuid = Store.objects.get(store_id=1).store_uuid
    
    """
    Material Stock Test
    """

    def test_material_stock_view_create(self):
        url = reverse('creatematerialstock',kwargs={"store_uuid":self.uuid,"material_uuid":self.uuid})
        request = self.factory.post(url, data={"current_capacity":100,"max_capacity":250})
        view = MaterialStockViewSet.as_view({"post":"create"})
        force_authenticate(request,self.user)
        store_uuid = Store.objects.get(store_id=1).store_uuid
        material_uuid = Material.objects.get(material_id=1).material_uuid
        response = view(request,store_uuid = store_uuid,material_uuid=material_uuid)
        self.assertEqual(response.data["current_capacity"],100)
        self.assertEqual(response.data["max_capacity"],250)

    def test_material_stock_view_create_fail(self):
        url = reverse('creatematerialstock',kwargs={"store_uuid":self.uuid,"material_uuid":self.uuid})
        request = self.factory.post(url, data={"current_capacity":100,"max_capacity":250})
        view = MaterialStockViewSet.as_view({"post":"create"})
        force_authenticate(request,self.user)
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            store_uuid = Store.objects.get(store_id=3).store_uuid
            material_uuid = Material.objects.get(material_id=4).material_uuid
            view(request,store_uuid = store_uuid,material_uuid=material_uuid)
       
    def test_material_stock_view_list(self):
        url = reverse('listmaterialstock',kwargs={"store_uuid":self.uuid})
        request = self.factory.get(url)
        view = MaterialStockViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user=self.user)
        store_uuid = Store.objects.get(store_id=1).store_uuid
        response= view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
    
    def test_material_stock_view_list_fail(self):
        url = reverse('listmaterialstock',kwargs={"store_uuid":self.uuid})
        request = self.factory.get(url)
        view = MaterialStockViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user=self.user)
        store_uuid = Store.objects.get(store_id=2).store_uuid
        response= view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """
    Material Quantity Test
    """
    
    def test_material_quantity_view_list(self):
        url = reverse('listmaterialquantity', kwargs={"store_uuid":self.uuid,"product_uuid":self.uuid})
        request = self.factory.get(url)
        view = MaterialQuantityViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        store_uuid = Store.objects.get(store_id=1).store_uuid
        product_uuid = Product.objects.get(id=1).product_uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]["quantity"],5)
        self.assertEqual(response.data[0]["ingredient"]["name"],"wood")
        self.assertEqual(response.data[0]["product"]["name"],"Chair")
    
    def test_material_quantity_view_list_fail(self):
        url = reverse('listmaterialquantity', kwargs={"store_uuid":self.uuid,"product_uuid":self.uuid})
        request = self.factory.get(url)
        view = MaterialQuantityViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        store_uuid = Store.objects.get(store_id=2).store_uuid
        product_uuid = Product.objects.get(id=1).product_uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_material_quantity_view_create(self):
        url = reverse("creatematerialquantity", kwargs={"store_uuid":self.uuid,"product_uuid":self.uuid,"material_uuid":self.uuid})
        request = self.factory.post(url, data={"quantity":7})
        view = MaterialQuantityViewSet.as_view({"post":"create"})
        force_authenticate(request, user= self.user)
        store_uuid = Store.objects.get(store_id=1).store_uuid
        material_uuid = Material.objects.get(material_id=3).material_uuid
        product_uuid = Product.objects.get(id=1).product_uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid,material_uuid=material_uuid)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["quantity"],7)
        self.assertEqual(response.data["ingredient"]["name"],"steel")
        self.assertEqual(response.data["product"]["name"],"Chair")
    
    def test_material_quantity_view_create_fail(self):
        url = reverse("creatematerialquantity", kwargs={"store_uuid":self.uuid,"product_uuid":self.uuid,"material_uuid":self.uuid})
        request = self.factory.post(url, data={"quantity":7})
        view = MaterialQuantityViewSet.as_view({"post":"create"})
        force_authenticate(request, user= self.user)
        store_uuid = Store.objects.get(store_id=2).store_uuid
        material_uuid = Material.objects.get(material_id=3).material_uuid
        product_uuid = Product.objects.get(id=1).product_uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid,material_uuid=material_uuid)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    """
    Material Restock View Test
    """
    def test_material_restock_get_view(self):
        url = reverse("materialrestock", kwargs={"store_uuid":self.uuid,"material_stock_uuid":self.uuid})
        request = self.factory.get(url)
        view  = MaterialRestockViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        store_uuid = Store.objects.get(store_id = 1).store_uuid
        response = view(request,store_uuid = store_uuid)
        self.assertEqual(response.data[0]["quantity"], 96)
        self.assertEqual(response.data[0]["price"], "480.00")

    def test_material_restock_get_view_fail(self):
        url = reverse("materialrestock", kwargs={"store_uuid":self.uuid,"material_stock_uuid":self.uuid})
        request = self.factory.get(url)
        view  = MaterialRestockViewSet.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        store_uuid = Store.objects.get(store_id = 2).store_uuid
        response = view(request,store_uuid = store_uuid)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


    def test_material_restock_post_view(self):
        url = reverse("materialrestock", kwargs={"store_uuid":self.uuid,"material_stock_uuid":self.uuid})
        request = self.factory.post(url)
        view  = MaterialRestockViewSet.as_view({"post":"create"})
        force_authenticate(request, user = self.user)
        store_uuid = Store.objects.get(store_id = 1).store_uuid
        response = view(request,store_uuid = store_uuid)
        self.assertEqual(response.data[0]["restocked_amount"], 96)
        self.assertEqual(response.data[0]["price"], "480.00")

    def test_material_restock_post_view_fail(self):
        url = reverse("materialrestock", kwargs={"store_uuid":self.uuid,"material_stock_uuid":self.uuid})
        request = self.factory.post(url)
        view  = MaterialRestockViewSet.as_view({"post":"create"})
        force_authenticate(request, user = self.user)
        store_uuid = Store.objects.get(store_id = 2).store_uuid
        response = view(request,store_uuid = store_uuid)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)