from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Account.serializer.AccountSerializer import UserSerializer, UserAuthSerializer 
from Account.services.account_services import get_user,create_user,sign_out_user

# Create your views here.
class UserView(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self,pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404

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
        return Response({"error":"You can't retrieve user detail of others"},status=status.HTTP_400_BAD_REQUEST)
    

class UserCreateView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[AllowAny]

    def create(self,request):
        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            token = create_user(serializer=serializer)
            if token:
                return Response(token.key, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



