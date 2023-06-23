from rest_framework import status
from rest_framework.response import Response

from .models import MaterialStock,Material,MaterialQuantity
from .serializer.MaterialSerializer import MaterialStockSerializer, MaterialSerializer, MaterialQuantitySerializer, MaterialRestockSerializer, RestockedSerializer
from .services.material_services import ( list_material_stock_service, create_material_stock_service ,list_material_quantity_service, create_material_quantity_service)

from Store.services.store_services import get_store_service
from IM_server.views import BaseAuthenticatedViewSet

# Create your views here.
class MaterialViewSet(BaseAuthenticatedViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    lookup_field = "material_uuid"
    

class MaterialStockViewSet(BaseAuthenticatedViewSet):
    queryset = MaterialStock.objects.all()
    serializer_class = MaterialStockSerializer
    lookup_field = "material_stock_uuid"

    def create(self, request, store_uuid, material_uuid):
        material_stock = create_material_stock_service(request, store_uuid, material_uuid) 
        if not material_stock:
             return Response({"error":"Fail To Create Material Stock"},
                            status = status.HTTP_400_BAD_REQUEST)
        return Response(MaterialStockSerializer(material_stock, many = False).data,
                        status = status.HTTP_201_CREATED)

    def retrieve(self, request, store_uuid):
        material_stock = list_material_stock_service(request, store_uuid)
        if not material_stock:
            return Response({"error":"Inventory Empty"},
                            status = status.HTTP_404_NOT_FOUND)
        return Response(MaterialStockSerializer(material_stock, many = True).data,
                        status = status.HTTP_200_OK)


    

class MaterialQuantityViewSet(BaseAuthenticatedViewSet):
    queryset = MaterialQuantity.objects.all()
    serializer_class = MaterialQuantitySerializer
    lookup_field = "material_quantity_uuid"

    def create(self, request, store_uuid, material_uuid, product_uuid):
        material_quantity = create_material_quantity_service(request, store_uuid, material_uuid, product_uuid)
        if not material_quantity:
             return Response({"error":"Fail To Create Material Quantity"},
                            status = status.HTTP_400_BAD_REQUEST)
        return Response(MaterialQuantitySerializer(material_quantity, many = False).data,
                        status = status.HTTP_201_CREATED)
    
    def retrieve(self,request,store_uuid,product_uuid):
        material_quantity = list_material_quantity_service(request,store_uuid,product_uuid)
        if not material_quantity:
             return Response({"error":"Material Quantity Not Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(MaterialQuantitySerializer(material_quantity, many = True).data,
                        status = status.HTTP_200_OK)
    

class MaterialRestockViewSet(BaseAuthenticatedViewSet):
    queryset = MaterialStock.objects.all()
    serializer_class = MaterialRestockSerializer

    def retrieve(self, request, store_uuid):
        
            store = get_store_service(request.user, store_uuid)
            material_stock = MaterialStock.objects.filter(store = store)
            if not material_stock:
                return Response({"error":"No Material Stock Found"},
                            status=status.HTTP_404_NOT_FOUND)
            serialized_objs = MaterialRestockSerializer(material_stock, many = True).data
            total_price = [obj["price"] for obj in serialized_objs if obj["price"]!="-"]
            return Response({"total price":sum(total_price) ,"restock material":serialized_objs}, 
                            status = status.HTTP_200_OK)
        # except:
        #     return Response({"error":"No Material Stock Found"},
        #                     status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request, store_uuid):
        try:
            store = get_store_service(request.user, store_uuid)
            material_stock = MaterialStock.objects.filter(store = store)
            if not material_stock:
                return Response({"error":"Fail To Restock"},
                            status=status.HTTP_400_BAD_REQUEST)
            serialized_objs = RestockedSerializer(material_stock,many = True).data
            total_price = [obj["price"] for obj in serialized_objs if obj["price"]!="-"]
            return Response({"total price":sum(total_price) ,"restock material":serialized_objs}, 
                            status = status.HTTP_200_OK)
        except:
             return Response({"error":"Fail To Restock"},
                            status=status.HTTP_400_BAD_REQUEST)

