from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product,Store
from .serializer.store_serializer import StoreSerializer,ProductSerializer,RemainingCapacitySerializer
from .services.store_services import (get_stores_service, get_store_service, 
list_product_service, create_product_service, create_store_service,
product_sales_services)

from Material.models import MaterialStock
from Material.serializer.MaterialSerializer import MaterialStockSerializer

# Create your views here.
class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    lookup_field = "store_uuid"

    def retrieve(self,request,store_uuid=None):
        error={}
        if not store_uuid:
            store = get_stores_service(request.user)
            if not store:
                error["error"] = "This User Didn't Have A Store Yet"
                return Response(error,status=status.HTTP_404_NOT_FOUND)
            serializedStore = StoreSerializer(store, many=True)
        else:
            store = get_store_service(request.user,store_uuid)
            if not store:
                error["error"] = "Store Not Found"
                return Response(error,status=status.HTTP_404_NOT_FOUND)
            serializedStore = StoreSerializer(store, many=False)
        return Response(serializedStore.data,status=status.HTTP_200_OK)
    
    def create(self, request):
        store = create_store_service(request)
        if not store:
            return Response({"error":"Fail To Create store"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(StoreSerializer(store,many=False).data, status = status.HTTP_200_OK)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "product_uuid"

    def create(self, request,store_uuid):
        product = create_product_service(request,store_uuid)
        if not product:
            return Response({"error":"Fail To Create Product"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductSerializer(product,many=False).data, status = status.HTTP_200_OK)

    def retrieve(self,request,store_uuid):
        product = list_product_service(request,store_uuid)
        if not product:
            return Response({"error":"No Product"}, status = status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product, many = True).data, status = status.HTTP_200_OK)
    
   
class ProductCapacityViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = RemainingCapacitySerializer
    
    def retrieve(self,request,store_uuid):
        product = list_product_service(request,store_uuid)
        store = get_store_service(request.user,store_uuid )
        if not product:
            return Response({"error":"No Product"}, status = status.HTTP_404_NOT_FOUND)
        return Response(RemainingCapacitySerializer(product, many = True,context={'store': store}).data, status = status.HTTP_200_OK)
    

class SalesViewSet(ModelViewSet):
    queryset = MaterialStock.objects.all()
    serializer_class = MaterialStockSerializer

    def create(self,request,store_uuid):
        response = product_sales_services(request = request, store_uuid = store_uuid)
        if response["sale"] == []:
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        return Response(response, status = status.HTTP_200_OK)