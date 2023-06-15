from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory,APITestCase,force_authenticate

from TestSetUp.testsetup import initialAccountStoreSetUp,initialProductSetUp
from Material.views import  MaterialView,MaterialStockView,MaterialQuantityView


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
        url = reverse("list_material")
        request = self.factory.post(url, data={"name":"glass","price":14.30})
        view  = MaterialView.as_view({"post":"create"})
        force_authenticate(request,user=self.user)
        response = view(request)
        self.assertEqual(response.data['name'],'glass')
        self.assertEqual(response.data["price"], "14.30")
    
    def test_material_view_list(self):
        url = reverse("list_material")
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
        url = reverse("material",kwargs={"material_id":3})
        request = self.factory.put(url,data={"name":"steel","price":14.30})
        view  =MaterialView.as_view({"put":"update"})
        force_authenticate(request,user=self.user)
        response = view(request,material_id=3)
        self.assertEqual(response.data['name'],'steel')
        self.assertEqual(response.data["price"], "14.30")
    
    def test_material_view_update_fail(self):
        url = reverse("material",kwargs={"material_id":4})
        request = self.factory.put(url,data={"name":"steel","price":14.30})
        view  =MaterialView.as_view({"put":"update"})
        force_authenticate(request,user=self.user)
        response = view(request,material_id=4)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_material_view_delete(self):
        url = reverse("material",kwargs={"material_id":1})
        request = self.factory.delete(url)
        view  =MaterialView.as_view({"delete":"destroy"})
        force_authenticate(request,user=self.user)
        response = view(request,material_id=1)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_material_view_delete_fail(self):
        url = reverse("material",kwargs={"material_id":4})
        request = self.factory.delete(url)
        view  =MaterialView.as_view({"delete":"destroy"})
        force_authenticate(request,user=self.user)
        response = view(request,material_id=4)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    """
    Material Stock Test
    """

    def test_material_stock_view_create(self):
        url = reverse('create_material_stock',kwargs={"store_id":1,"material_id":1})
        request = self.factory.post(url, data={"current_capacity":100,"max_capacity":250})
        view = MaterialStockView.as_view({"post":"create"})
        force_authenticate(request,self.user)
        response = view(request,store_id = 1,material_id=1)
        self.assertEqual(response.data["current_capacity"],100)
        self.assertEqual(response.data["max_capacity"],250)

    def test_material_stock_view_create_fail(self):
        url = reverse('create_material_stock',kwargs={"store_id":1,"material_id":1})
        request = self.factory.post(url, data={"current_capacity":100,"max_capacity":250})
        view = MaterialStockView.as_view({"post":"create"})
        force_authenticate(request,self.user)
        response = view(request,store_id = 3,material_id=4)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_material_stock_view_list(self):
        url = reverse('list_material_stock',kwargs={"store_id":1})
        request = self.factory.get(url)
        view = MaterialStockView.as_view({"get":"retrieve"})
        force_authenticate(request,user=self.user)
        response= view(request,store_id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
    
    def test_material_stock_view_list_fail(self):
        url = reverse('list_material_stock',kwargs={"store_id":2})
        request = self.factory.get(url)
        view = MaterialStockView.as_view({"get":"retrieve"})
        force_authenticate(request,user=self.user)
        response= view(request,store_id=2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_material_stock_view_max_capacity_update(self):
        url = reverse('material_stock',kwargs={"store_id":1,"material_stock_id":1})
        request = self.factory.put(url, data={"max_capacity":250})
        view = MaterialStockView.as_view({"put":"update"})
        force_authenticate(request,self.user)
        response = view(request,store_id = 1,material_stock_id=1)
        self.assertEqual(response.data["current_capacity"],104)
        self.assertEqual(response.data["max_capacity"],250)
        
    def test_material_stock_view_max_capacity_update_fail(self):
        url = reverse('material_stock',kwargs={"store_id":1,"material_stock_id":3})
        request = self.factory.put(url, data={"max_capacity":250})
        view = MaterialStockView.as_view({"put":"update"})
        force_authenticate(request,self.user)
        response = view(request,store_id = 1,material_stock_id=3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_material_stock_view_delete(self):
        url = reverse('material_stock',kwargs={"store_id":1,"material_stock_id":1})
        request = self.factory.delete(url)
        view = MaterialStockView.as_view({"delete":"destroy"})
        force_authenticate(request,self.user)
        response = view(request,store_id = 1,material_stock_id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_material_stock_view_delete_fail(self):
        url = reverse('material_stock',kwargs={"store_id":1,"material_stock_id":1})
        request = self.factory.delete(url)
        view = MaterialStockView.as_view({"delete":"destroy"})
        force_authenticate(request,self.user2)
        response = view(request,store_id = 1,material_stock_id=1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """
    Material Quantity Test
    """
    
    def test_material_quantity_view_list(self):
        url = reverse('list_material_quantity', kwargs={"store_id":1,"product_id":1})
        request = self.factory.get(url)
        view = MaterialQuantityView.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        response = view(request,store_id=1,product_id=1)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]["quantity"],5)
        self.assertEqual(response.data[0]["ingredient"]["name"],"wood")
        self.assertEqual(response.data[0]["product"]["name"],"Chair")
    
    def test_material_quantity_view_list_fail(self):
        url = reverse('list_material_quantity', kwargs={"store_id":2,"product_id":1})
        request = self.factory.get(url)
        view = MaterialQuantityView.as_view({"get":"retrieve"})
        force_authenticate(request,user = self.user)
        response = view(request,store_id=2,product_id=1)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_material_quantity_view_create(self):
        url = reverse("create_material_quantity", kwargs={"store_id":1,"product_id":1,"material_id":3})
        request = self.factory.post(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"post":"create"})
        force_authenticate(request, user= self.user)
        response = view(request,store_id=1,product_id=1,material_id=3)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data["quantity"],7)
        self.assertEqual(response.data["ingredient"]["name"],"steel")
        self.assertEqual(response.data["product"]["name"],"Chair")
    
    def test_material_quantity_view_create_fail(self):
        url = reverse("create_material_quantity", kwargs={"store_id":2,"product_id":1,"material_id":3})
        request = self.factory.post(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"post":"create"})
        force_authenticate(request, user= self.user)
        response = view(request,store_id=2,product_id=1,material_id=3)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_material_quantity_view_update(self):
        url = reverse("material_quantity", kwargs={"store_id":2,"product_id":1,"material_id":3,"material_quantity_id":1})
        request = self.factory.put(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"put":"update"})
        force_authenticate(request, user= self.user)
        response = view(request,store_id=1,product_id=1,material_id=1,material_quantity_id=1)
        self.assertEqual(response.data["quantity"],7)
        self.assertEqual(response.data["ingredient"]["name"],"wood")
        self.assertEqual(response.data["product"]["name"],"Chair")

    def test_material_quantity_view_update_fail(self):
        url = reverse("material_quantity", kwargs={"store_id":2,"product_id":1,"material_id":3,"material_quantity_id":1})
        request = self.factory.put(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"put":"update"})
        force_authenticate(request, user= self.user)
        response = view(request,store_id=2,product_id=1,material_id=1,material_quantity_id=1)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_material_quantity_view_delete(self):
        url = reverse("material_quantity", kwargs={"store_id":1,"product_id":1,"material_id":1,"material_quantity_id":1})
        request = self.factory.delete(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"delete":"destroy"})
        force_authenticate(request, user= self.user)
        response = view(request,store_id=1,product_id=1,material_id=1,material_quantity_id=1)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_material_quantity_view_delete_fail(self):
        url = reverse("material_quantity", kwargs={"store_id":2,"product_id":3,"material_id":1,"material_quantity_id":1})
        request = self.factory.delete(url, data={"quantity":7})
        view = MaterialQuantityView.as_view({"delete":"destroy"})
        force_authenticate(request, user= self.user)
        response = view(request,store_id=2,product_id=3,material_id=1,material_quantity_id=1)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)