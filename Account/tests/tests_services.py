from django.test import TestCase
from Account.models import User
from TestSetUp.testsetup import initialAccountStoreSetUp
from Services.AccountService.account_services import*

class TestAccountService(TestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)

    def test_auth_user_success(self):
        request = self.client.request().wsgi_request
        request.method= "POST"
        request.data= {"username":"UncleBen"}
        response = auth_user(request)
        self.assertEqual(response,Token.objects.get(user=User.objects.get(id=1)).key)


    def test_auth_user_error_wrong_name(self):  
        request = self.client.request().wsgi_request
        request.method= "POST"
        request.data = {"username":"Uncle_ben"}
        self.assertFalse(auth_user(request))

    def test_auth_user_error_name_isNone(self):
        request = self.client.request().wsgi_request
        request.method= "POST"
        request.data = {"username":None}
        self.assertFalse(auth_user(request))

    def test_get_user_success(self):
        request = self.client.request().wsgi_request
        request.user = User.objects.get(id=1)
        get_user(request)
    
    def test_get_user_error(self):
        request = self.client.request().wsgi_request
        self.assertFalse(get_user(request))

    def test_get_stores_success(self):
        user = User.objects.get(id=1)
        get_stores(user)

    def test_get_stores_fail(self):
        user = User.objects.get(id=3)
        self.assertFalse(get_stores(user))
    
    def test_get_store_with_id_success(self):
        user =  User.objects.get(id=1)
        get_store(user,1)
    
    def test_get_store_with_id_fail(self):
        user = User.objects.get(id=2)
        self.assertFalse(get_store(user,1))
    
    def test_get_store_no_store_fail(self):
        user = User.objects.get(id=3)
        self.assertFalse(get_store(user,1))

    

    


