from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from Account.models import User
from Material.models import Store
from Serializer.MaterialSerializer.MaterialSerializer import StoreSerializer
from rest_framework.authtoken.models import Token
from Services.AccountService.account_services import auth_user,get_stores,get_store

# Create your views here.
@api_view(['POST'])
def authenticateUser(request):
    error={}
    token = auth_user(request)
    if(token):
        return Response({"Token":"{}".format(token)},status=status.HTTP_200_OK)
    error["error"] = "Could't Get The User"
    return Response(error,status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getStores(request):
    error={}
    store = get_stores(request.user)
    if not store:
        error["error"] = "This User Didn't Have A Store Yet"
        return Response(error,status=status.HTTP_400_BAD_REQUEST)
    serializedStore = StoreSerializer(store, many=True)
    return Response(serializedStore.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getStore(request,id):
    error={}
    store = get_store(request.user,id)
    if not store:
        error["error"] = "Store Not Found"
        return Response(error,status=status.HTTP_400_BAD_REQUEST)
    serializedStore = StoreSerializer(store, many=False)
    return Response(serializedStore.data,status=status.HTTP_200_OK)


