from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout

from rest_framework.permissions import AllowAny
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from .serializer.AccountSerializer import UserSerializer, UserAuthSerializer 
from .services.account_services import get_user,create_user,sign_out_user
from .authentication import CustomSessionAuthentication, CheckIfAuthenticate


# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self,request):
        user=get_user(request)
        if(user):
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error":"You can't retrieve user detail of others"},status=status.HTTP_400_BAD_REQUEST)
    
    def create(self,request):
        user = get_user(request)
        response = sign_out_user(user)
        if response:
             return Response({"success":"Sign Out Successfully"}, status=status.HTTP_200_OK)
        return Response({"error":"Fail To Sign Out"},status=status.HTTP_400_BAD_REQUEST)
    

class UserCreateViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[AllowAny]
    authentication_classes=[]

    def create(self,request):
        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            token = create_user(serializer=serializer)
            if token:
                return Response(token.key, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthTokenView(ObtainAuthToken):
    permission_classes=[AllowAny]
    authentication_classes=[]

"""
Template View
"""

class ObtainAuthTokenTemplateView(ObtainAuthToken):
    permission_classes=[AllowAny]
    authentication_classes=[CheckIfAuthenticate]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'auth_template/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("liststorestemplate")
        serializer = UserAuthSerializer()
        return Response({"serializer": serializer})
    
    def post(self, request, *args, **kwargs):
        serializer = UserAuthSerializer(data = request.data)
        if serializer.is_valid():
            user = authenticate(request = request, username = serializer.data["username"], password = serializer.data["password"])
            if user:
                login(request, user)
                return redirect("liststorestemplate")
            return Response({"serializer": serializer, "error":"login failed"})
        return Response({"serializer": serializer, "error":"missing username or password"})


class LogOutTemplateViewSet(ModelViewSet):
    authentication_classes=[CustomSessionAuthentication]

    def destroy(self, request):
        logout(request)
        return Response({"response":"logout successful"})
    

class RegisterTemplateViewSet(ModelViewSet):
    permission_classes=[AllowAny]
    authentication_classes=[CheckIfAuthenticate]
    renderer_classes = [TemplateHTMLRenderer]
    queryset = User.objects.all()
    lookup_field = ""
    template_name = 'auth_template/register.html'

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("liststorestemplate")
        serializer = UserAuthSerializer()
        return Response({"serializer": serializer})

    def create(self,request):
        try:
            serializer = UserAuthSerializer(data=request.data)
            if serializer.is_valid():
                user = User.objects.create_user(username = serializer.data["username"], password = serializer.data["password"])
                if user:
                    return redirect("authenticateusertemplate")
        except:
           return Response({"serializer": serializer, "error":"username taken"})
