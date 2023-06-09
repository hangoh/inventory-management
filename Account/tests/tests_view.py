from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from Account.models import User
from Material.models import Store
from rest_framework.authtoken.models import Token
from Account.views import getStores,getStore
from rest_framework.test import force_authenticate,APIRequestFactory
from TestSetUp.testsetup import initialAccountStoreSetUp

class UserTest(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        self.factory = APIRequestFactory()

    def test_authenticateUser_success(self):
        url = reverse('authenticateUser')
        data={"username":"UncleBen"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.get(key=response.data.get("Token")).user, User.objects.get(id=1))

    def test_authenticateUser_fail(self):
        url = reverse('authenticateUser')
        data={"username":"Uncleben"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("error"),"Could't Get The User")

    def test_getStores_success(self):
        url=reverse("store")
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = getStores
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
        url=reverse("store")
        user = User.objects.get(id=3)
        request = self.factory.get(url)
        view = getStores
        force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_getStores_unauthorized_fail(self):
        url=reverse("store")
        request = self.factory.get(url)
        view = getStores
        force_authenticate(request)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_getStore_success(self):
        url=reverse("store")
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = getStore
        force_authenticate(request,user=user)
        response = view(request,id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["store_id"], 1)
        self.assertEqual(response.data["store_name"], "UncleBen'S")
    
    def test_getStore_store_not_found_fail(self):
        url=reverse("store")
        user = User.objects.get(id=1)
        request = self.factory.get(url)
        view = getStore
        force_authenticate(request,user=user)
        response = view(request,id=3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_getStore_store_no_store_fail(self):
        url=reverse("store")
        user = User.objects.get(id=3)
        request = self.factory.get(url)
        view = getStore
        force_authenticate(request,user=user)
        response = view(request,id=3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_getStore_store_unauthorized_fail(self):
        url=reverse("store")
        request = self.factory.get(url)
        view = getStore
        force_authenticate(request)
        response = view(request,id=3)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

       
    