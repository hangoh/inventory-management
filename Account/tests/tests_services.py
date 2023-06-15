from django.test import TestCase
from django.contrib.auth.models import User

from Account.serializer.AccountSerializer import UserAuthSerializer
from Account.services.account_services import get_user,create_user,login_user
from TestSetUp.testsetup import initialAccountStoreSetUp


class TestAccountService(TestCase):
    def setUp(self):
        super().setUp()
        initialAccountStoreSetUp(self)

    def test_get_user_success(self):
        request = self.client.request().wsgi_request
        request.user = User.objects.get(id=1)
        get_user(request)
    
    def test_get_user_error(self):
        request = self.client.request().wsgi_request
        self.assertFalse(get_user(request))
    
    def test_create_user_success(self):
        serializer =UserAuthSerializer({"username":"UncleD","password":"JustPassword"})
        create_user(serializer=serializer)
 
    def test_login_user_success(self):
        serializer =UserAuthSerializer({"username":"UncleBen","password":"JustPassword"})
        login_user(serializer=serializer)

    def test_login_user_fail(self):
        serializer =UserAuthSerializer({"username":"UncleBen","password":"justPassword"})
        self.assertFalse(login_user(serializer=serializer))