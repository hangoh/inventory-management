from django.urls import reverse
from rest_framework.test import APITestCase,force_authenticate,APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from TestSetUp.testsetup import initialAccountStoreSetUp
from Account.views import UserView

class UserTest(APITestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)
        self.factory = APIRequestFactory()

    def test_authenticateUser_success(self):
        url = reverse('authenticate_user')
        data={"username":"UncleBen", "password":"JustPassword"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticateUser_fail(self):
        url = reverse('authenticate_user')
        data={"username":"Uncleben", "password":"JustPassword"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_user_success(self):
        url = reverse('user')
        user= User.objects.get(id=1)
        request = self.factory.get(url)
        request.user= user
        view = UserView.as_view({"get":"retrieve"})
        force_authenticate(request,user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"],"UncleBen")
    
    def test_get_user_unauthorized_fail(self):
        url = reverse('user')
        user= User.objects.get(id=1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_user_success(self):
        url = reverse('user_sign_up')
        data={'username':'UncleB',"password":"JustPassword"}
        response= self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

    def test_create_user_fail(self):
        url = reverse('user_sign_up')
        data={'username':'UncleBen',"password":"JustPassword"}
        with self.assertRaises(IntegrityError):
            response= self.client.post(url,data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

