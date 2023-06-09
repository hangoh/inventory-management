from rest_framework import authentication
from django_mock_queries.query import MockModel,MockSet
from unittest import mock
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework.test import APIRequestFactory,APITestCase



class AuthenticationTest(authentication.TokenAuthentication):
    word="Test_Token"
    def authenticate(self, request,token): 
        http = request.META.get("AUTH")
        if not http:
             raise exceptions.AuthenticationFailed("No AUTH in header")
        auth_token = http.split()
        if auth_token[0]!=self.word or len(auth_token)!=2:
            raise exceptions.AuthenticationFailed("Incorrect Token Format")
        token_key = auth_token[1]
        try:
            token = Token.objects.get(key = token_key)
            user = token.user
        except:
            raise exceptions.AuthenticationFailed("Token does not exist")
        return (user,token)

class TestAuth(APITestCase):
    factory = APIRequestFactory()
    url=reverse("authenticateUser")
    def setUp(self):
        super().setUp()
        users=MockSet(
        MockModel(id=1,name="UncleBen"),
        MockModel(id=2,name="UncleBob")
            )
        keys = MockSet(
            MockModel(user = users.get(name="UncleBen"), key="UncleBen_Key"),
            MockModel(user = users.get(name="UncleBob"), key="UncleBob_Key")
        )
        self.user_objects=mock.patch("Account.models.User.objects",users).start()
        self.token_objects=mock.patch("rest_framework.authtoken.models.Token.objects",keys).start()


    def test_auth_success(self):
        request = self.factory.post(self.url,AUTH = "Test_Token UncleBen_Key")
        auth = AuthenticationTest()
        user,token = auth.authenticate(request,self.token_objects)
        self.assertEqual(user.name,"UncleBen")
        self.assertEqual(token.key,"UncleBen_Key")
    
    def test_auth_unsuccessfull_wrong_token(self):
        request = self.factory.post(self.url,AUTH = "Test_Token Uncleben_Key")
        auth = AuthenticationTest()
        with self.assertRaises(exceptions.AuthenticationFailed):
            auth.authenticate(request,self.token_objects)
    
    def test_auth_unsuccessfull_wrong_token_format(self):
        request = self.factory.post(self.url,AUTH = "Token UncleBen_Key")
        auth = AuthenticationTest()
        with self.assertRaises(exceptions.AuthenticationFailed):
            auth.authenticate(request,self.token_objects)
    
    def test_auth_unsuccessfull_no_token(self):
        request = self.factory.post(self.url)
        auth = AuthenticationTest()
        with self.assertRaises(exceptions.AuthenticationFailed):
            auth.authenticate(request,self.token_objects)
        
        

    

    