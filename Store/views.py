from rest_framework import status
from rest_framework.response import Response

from .models import Product,Store
from .serializer.store_serializer import StoreSerializer,ProductSerializer,RemainingCapacitySerializer
from .services.store_services import (get_stores_service, get_store_service, 
list_product_service, update_store_name_service, delete_store_service, 
update_product_name_service, delete_product_service, create_store, create_product_service,
product_sales_services)

from IM_server.views import BaseAuthenticatedViewSet
from Material.models import MaterialStock
from Material.serializer.MaterialSerializer import MaterialStockSerializer

# Create your views here.
class StoreViewSet(BaseAuthenticatedViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def create(self, request):
        store = create_store(request)
        if not store:
            return Response({"error":"Fail To Create Store"},status=status.HTTP_400_BAD_REQUEST)
        return Response(StoreSerializer(store, many=False).data,status=status.HTTP_200_OK)

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

    def update(self,request,store_uuid):
        store = update_store_name_service(request,store_uuid)
        if not store:
             return Response({"error":"Failed to Update Store Name"},status=status.HTTP_400_BAD_REQUEST)
        return Response(StoreSerializer(store, many=False).data,status=status.HTTP_200_OK)
    
    def destroy(self,request,store_uuid):
        store = delete_store_service(request,store_uuid)
        if not store:
             return Response({"error":"Failed to Delete Store"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"response":"Delete Store Successfully"},status=status.HTTP_200_OK)
    

class ProductViewSet(BaseAuthenticatedViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request,store_uuid):
        product = create_product_service(request,store_uuid)
        if not product:
            return Response({"error":"Fail To Create Product"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductSerializer(product,many=False).data, status = status.HTTP_200_OK)

    def retrieve(self,request,store_uuid):
        product = list_product_service(request,store_uuid)
        if not product:
            return Response({"error":"No Product"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product,many=True).data, status = status.HTTP_200_OK)
    
    def update(self,request,store_uuid,product_uuid):
        product = update_product_name_service(request,store_uuid,product_uuid)
        if not product:
             return Response({"error":"Product Not Available"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductSerializer(product,many=False).data, status = status.HTTP_200_OK)
    
    def destroy(self,request,store_uuid,product_uuid):
        product = delete_product_service(request,store_uuid,product_uuid)
        if not product:
             return Response({"error":"Failed to Delete Product"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"response":"Delete Product Successfully"}, status = status.HTTP_200_OK)
    

class ProductCapacityViewSet(BaseAuthenticatedViewSet):
    queryset = Product.objects.all()
    serializer_class = RemainingCapacitySerializer
    
    def retrieve(self,request,store_uuid):
        product = list_product_service(request,store_uuid)
        if not product:
            return Response({"error":"No Product"}, status = status.HTTP_404_NOT_FOUND)
        return Response(RemainingCapacitySerializer(product,many=True).data, status = status.HTTP_200_OK)
    

class SalesViewSet(BaseAuthenticatedViewSet):
    queryset = MaterialStock.objects.all()
    serializer_class = MaterialStockSerializer

    def create(self,request,store_uuid):
        response = product_sales_services(request = request, store_uuid = store_uuid)
        if response["sale"] == []:
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        return Response(response, status = status.HTTP_200_OK)