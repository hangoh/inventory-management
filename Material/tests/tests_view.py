from django.urls import reverse
from django.core import exceptions

from rest_framework import status
from rest_framework.test import APIRequestFactory,APITestCase,force_authenticate

from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Material.views import  MaterialView,MaterialStockView,MaterialQuantityView
from Material.models import Material,MaterialQuantity,MaterialStock
from Store.models import Store,Product

class TestMaterialView(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        initialProductSetUp(self)
        self.factory = APIRequestFactory()

    """
    Material View Test
    """

    def test_material_view_create(self):
        url = reverse("listmaterial")
        request = self.factory.post(url, data={"name":"glass","price":14.30})
        view  = MaterialView.as_view({"post":"create"})
        force_authenticate(request,user=self.user)
        response = view(request)
        self.assertEqual(response.data['name'],'glass')
        self.assertEqual(response.data["price"], "14.30")
    
    def test_material_view_list(self):
        url = reverse("listmaterial")
        request = self.factory.get(url)
        view  = MaterialView.as_view({"get":"retrieve"})
        force_authenticate(request,user=self.user)
        response = view(request)
        expected_result_array = [
            {"material_id":1,"price":"5.00","name":"wood"},
            {"material_id":2,"price":"1.30","name":"plastic"},
            {"material_id":3,"price":"10.50","name":"steel"}
        ]
        i=0
        for r in response.data:
            self.assertEqual(r["price"],expected_result_array[i]["price"])
            self.assertEqual(r["name"],expected_result_array[i]["name"])
            i+=1

    def test_material_view_update(self):
        url = reverse("material",kwargs={"material_uuid":3})
        request = self.factory.put(url,data={"name":"steel","price":14.30})
        view  =MaterialView.as_view({"put":"update"})
        force_authenticate(request,user=self.user)
        material_uuid = Material.objects.get(material_id=3).uuid
        response = view(request,material_uuid=material_uuid)
        self.assertEqual(response.data['name'],'steel')
        self.assertEqual(response.data["price"], "14.30")
    
    def test_material_view_update_fail(self):
        url = reverse("material",kwargs={"material_uuid":4})
        request = self.factory.put(url,data={"name":"steel","price":14.30})
        view  =MaterialView.as_view({"put":"update"})
        force_authenticate(request,user=self.user)
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            material_uuid = Material.objects.get(material_id=4).uuid
            view(request,material_uuid=material_uuid)
    
    def test_material_view_delete(self):
        url = reverse("material",kwargs={"material_uuid":1})
        request = self.factory.delete(url)
        view  =MaterialView.as_view({"delete":"destroy"})
        force_authenticate(request,user=self.user)
        material_uuid = Material.objects.get(material_id=1).uuid
        response = view(request,material_uuid=material_uuid)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_material_view_delete_fail(self):
        url = reverse("material",kwargs={"material_uuid":4})
        request = self.factory.delete(url)
        view  =MaterialView.as_view({"delete":"destroy"})
        force_authenticate(request,user=self.user)
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            material_uuid = Material.objects.get(material_id=4).uuid
            view(request,material_uuid=material_uuid)
    
    """
    Material Stock Test
    """

    def test_material_stock_view_create(self):
        url = reverse('creatematerialstock',kwargs={"store_uuid":1,"material_uuid":1})
        request = self.factory.post(url, data={"current_capacity":100,"max_capacity":250})
        view = MaterialStockView.as_view({"post":"create"})
        force_authenticate(request,self.user)
        store_uuid = Store.objects.get(store_id=1).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        response = view(request,store_uuid = store_uuid,material_uuid=material_uuid)
        self.assertEqual(response.data["current_capacity"],100)
        self.assertEqual(response.data["max_capacity"],250)

    def test_material_stock_view_create_fail(self):
        url = reverse('creatematerialstock',kwargs={"store_uuid":3,"material_uuid":4})
        request = self.factory.post(url, data={"current_capacity":100,"max_capacity":250})
        view = MaterialStockView.as_view({"post":"create"})
        force_authenticate(request,self.user)
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            store_uuid = Store.objects.get(store_id=3).uuid
            material_uuid = Material.objects.get(material_id=4).uuid
            view(request,store_uuid = store_uuid,material_uuid=material_uuid)
       
    def test_material_stock_view_list(self):
        url = reverse('listmaterialstock',kwargs={"store_uuid":1})
        request = self.factory.get(url)
        view = MaterialStockView.as_view({"get":"retrieve"})
        force_authenticate(request,user=self.user)
        store_uuid = Store.objects.get(store_id=1).uuid
        response= view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
    
    def test_material_stock_view_list_fail(self):
        url = reverse('listmaterialstock',kwargs={"store_uuid":2})
        request = self.factory.get(url)
        view = MaterialStockView.as_view({"get":"retrieve"})
        force_authenticate(request,user=self.user)
        store_uuid = Store.objects.get(store_id=2).uuid
        response= view(request,store_uuid=store_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_material_stock_view_max_capacity_update(self):
        url = reverse('materialstock',kwargs={"store_uuid":1,"material_stock_uuid":1})
        request = self.factory.put(url, data={"max_capacity":250})
        view = MaterialStockView.as_view({"put":"update"})
        force_authenticate(request,self.user)
        store_uuid = Store.objects.get(store_id=1).uuid
        material_stock_uuid = MaterialStock.objects.get(id=1).uuid
        response = view(request, store_uuid = store_uuid, material_stock_uuid=material_stock_uuid)
        self.assertEqual(response.data["current_capacity"],104)
        self.assertEqual(response.data["max_capacity"],250)
        
    def test_material_stock_view_max_capacity_update_fail(self):
        url = reverse('materialstock',kwargs={"store_uuid":1,"material_stock_uuid":3})
        request = self.factory.put(url, data={"max_capacity":250})
        view = MaterialStockView.as_view({"put":"update"})
        force_authenticate(request,self.user)
        store_uuid = Store.objects.get(store_id=1).uuid
        material_stock_uuid = MaterialStock.objects.get(id=3).uuid
        response = view(request,store_uuid = store_uuid,material_stock_uuid=material_stock_uuid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_material_stock_view_delete(self):
        url = reverse('materialstock',kwargs={"store_uuid":1,"material_stock_uuid":1})
        request = self.factory.delete(url)
        view = MaterialStockView.as_view({"delete":"destroy"})
        force_authenticate(request,self.user)
        store_uuid = Store.objects.get(store_id=1).uuid
        material_stock_uuid = MaterialStock.objects.get(id=1).uuid
        response = view(request,store_uuid = store_uuid,material_stock_uuid=material_stock_uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_material_stock_view_delete_fail(self):
        url = reverse('materialstock',kwargs={"store_uuid":1,"material_stock_uuid":1})
        request = self.factory.delete(url)
        view = MaterialStockView.as_view({"delete":"destroy"})
        force_authenticate(request,self.user2)
        store_uuid = Store.objects.get(store_id=1).uuid
        material_stock_uuid = MaterialStock.objects.get(id=1).uuid
        response = view(request,store_uuid = store_uuid, material_stock_uuid=material_stock_uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """
    Material Quantity Test
    """
    
    def test_material_quantity_view_list(self):
        url = reverse('listmaterialquantity', kwargs={"store_uuid":1,"product_uuid":1})
        request = self.factory.get(url)
        view = MaterialQuantityView.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        store_uuid = Store.objects.get(store_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]["quantity"],5)
        self.assertEqual(response.data[0]["ingredient"]["name"],"wood")
        self.assertEqual(response.data[0]["product"]["name"],"Chair")
    
    def test_material_quantity_view_list_fail(self):
        url = reverse('listmaterialquantity', kwargs={"store_uuid":2,"product_uuid":1})
        request = self.factory.get(url)
        view = MaterialQuantityView.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        store_uuid = Store.objects.get(store_id=2).uuid
        product_uuid = Product.objects.get(id=1).uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_material_quantity_view_create(self):
        url = reverse("creatematerialquantity", kwargs={"store_uuid":1,"product_uuid":1,"material_uuid":3})
        request = self.factory.post(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"post":"create"})
        force_authenticate(request, user= self.user)
        store_uuid = Store.objects.get(store_id=1).uuid
        material_uuid = Material.objects.get(material_id=3).uuid
        product_uuid = Product.objects.get(id=1).uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid,material_uuid=material_uuid)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["quantity"],7)
        self.assertEqual(response.data["ingredient"]["name"],"steel")
        self.assertEqual(response.data["product"]["name"],"Chair")
    
    def test_material_quantity_view_create_fail(self):
        url = reverse("creatematerialquantity", kwargs={"store_uuid":2,"product_uuid":1,"material_uuid":3})
        request = self.factory.post(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"post":"create"})
        force_authenticate(request, user= self.user)
        store_uuid = Store.objects.get(store_id=2).uuid
        material_uuid = Material.objects.get(material_id=3).uuid
        product_uuid = Product.objects.get(id=1).uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid,material_uuid=material_uuid)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_material_quantity_view_update(self):
        url = reverse("materialquantity", kwargs={"store_uuid":1,"product_uuid":1,"material_uuid":1,"material_quantity_uuid":1})
        request = self.factory.put(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"put":"update"})
        force_authenticate(request, user= self.user)
        store_uuid = Store.objects.get(store_id=1).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        material_quantity_uuid = MaterialQuantity.objects.get(id = 1).uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid,material_uuid=material_uuid,material_quantity_uuid=material_quantity_uuid)
        self.assertEqual(response.data["quantity"],7)
        self.assertEqual(response.data["ingredient"]["name"],"wood")
        self.assertEqual(response.data["product"]["name"],"Chair")

    def test_material_quantity_view_update_fail(self):
        url = reverse("materialquantity", kwargs={"store_uuid":3,"product_uuid":1,"material_uuid":1,"material_quantity_uuid":1})
        request = self.factory.put(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"put":"update"})
        force_authenticate(request, user= self.user)
        store_uuid = Store.objects.get(store_id=3).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        material_quantity_uuid = MaterialQuantity.objects.get(id = 1).uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid,material_uuid=material_uuid,material_quantity_uuid=material_quantity_uuid)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_material_quantity_view_delete(self):
        url = reverse("materialquantity", kwargs={"store_uuid":1,"product_uuid":1,"material_uuid":1,"material_quantity_uuid":1})
        request = self.factory.delete(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"delete":"destroy"})
        force_authenticate(request, user= self.user)
        store_uuid = Store.objects.get(store_id=1).uuid
        material_uuid = Material.objects.get(material_id=1).uuid
        product_uuid = Product.objects.get(id=1).uuid
        material_quantity_uuid = MaterialQuantity.objects.get(id = 1).uuid
        response = view(request,store_uuid=store_uuid,product_uuid=product_uuid,material_uuid=material_uuid,material_quantity_uuid=material_quantity_uuid)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_material_quantity_view_delete_fail(self):
        url = reverse("materialquantity", kwargs={"store_uuid":2,"product_uuid":3,"material_uuid":1,"material_quantity_uuid":1})
        request = self.factory.delete(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"delete":"destroy"})
        force_authenticate(request, user= self.user)
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            store_uuid = Store.objects.get(store_id=2).uuid
            material_uuid = Material.objects.get(material_id=1).uuid
            product_uuid = Product.objects.get(id=3).uuid
            material_quantity_uuid = MaterialQuantity.objects.get(id = 1).uuid
            response = view(request,store_uuid=store_uuid,product_uuid=product_uuid,material_uuid=material_uuid,material_quantity_uuid=material_quantity_uuid)
            self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)