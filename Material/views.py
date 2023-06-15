from rest_framework import status
from rest_framework.response import Response

from .models import MaterialStock,Material,MaterialQuantity
from .serializer.MaterialSerializer import MaterialStockSerializer,MaterialSerializer,MaterialQuantitySerializer
from .services.material_services import (list_material_service, update_material_service, create_material_service, delete_material_service, list_material_stock_service, update_max_capacity_service, create_material_stock_service ,delete_material_stock_service, list_material_quantity_service, update_material_quantity_service, create_material_quantity_service, delete_material_quantity_service)

from Account.views import BaseAuthenticatedView

# Create your views here.
class MaterialView(BaseAuthenticatedView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def create(self, request):
        material = create_material_service(request)
        if not material:
            return Response({"error":"Fail To Create Material"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(MaterialSerializer(material,many=False).data,
                        status=status.HTTP_201_CREATED)

    def retrieve(self,request):
        material = list_material_service()
        if not material:
            return Response({"error":"No Material Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(MaterialSerializer(material,many=True).data,
                        status=status.HTTP_200_OK)
    
    def update(self,request,material_id):
        material = update_material_service(request,material_id)
        if not material:
            return Response({"error":"Fail to Update Material"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(MaterialSerializer(material,many=False).data,
                        status=status.HTTP_200_OK)
    
    def destroy(self,request,material_id):
        material = delete_material_service(material_id)
        if not material:
            return Response({"error":"No Material Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"response":"Delete Material Successfully"},
                        status=status.HTTP_200_OK)


class MaterialStockView(BaseAuthenticatedView):
    queryset = MaterialStock.objects.all()
    serializer_class = MaterialStockSerializer

    def create(self,request,store_id,material_id):
        material_stock = create_material_stock_service(request,store_id,material_id) 
        if not material_stock:
             return Response({"error":"Fail To Create Material Stock"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(MaterialStockSerializer(material_stock,many=False).data,
                        status=status.HTTP_201_CREATED)

    def retrieve(self,request,store_id):
        material_stock = list_material_stock_service(request,store_id)
        if not material_stock:
            return Response({"error":"Inventory Empty"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(MaterialStockSerializer(material_stock, many=True).data,
                        status = status.HTTP_200_OK)

    def update(self, request,store_id,material_stock_id):
        material_stock = update_max_capacity_service(request,store_id,material_stock_id)
        if not material_stock:
            return Response({"error":"Fail to Update Inventory"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(MaterialStockSerializer(material_stock, many=False).data,
                        status = status.HTTP_200_OK)
    
    def destroy(self, request,store_id,material_stock_id):
        material_stock = delete_material_stock_service(request,store_id,material_stock_id)
        if not material_stock:
            return Response({"error":"No Inventory Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"response":"Delete Inventory Successfully"},
                        status=status.HTTP_200_OK)


class MaterialQuantityView(BaseAuthenticatedView):
    queryset = MaterialQuantity.objects.all()
    serializer_class = MaterialQuantitySerializer

    def create(self,request,store_id, material_id,product_id,):
        material_quantity = create_material_quantity_service(request,store_id, material_id,product_id)
        if not material_quantity:
             return Response({"error":"Fail To Create Material Quantity"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(MaterialQuantitySerializer(material_quantity,many=False).data,
                        status=status.HTTP_201_CREATED)
    
    def update(self,request,store_id, material_id,product_id,material_quantity_id):
        material_quantity = update_material_quantity_service(request,store_id, material_id,product_id,material_quantity_id)
        if not material_quantity:
             return Response({"error":"Fail To Update Material Quantity"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(MaterialQuantitySerializer(material_quantity,many=False).data,
                        status=status.HTTP_200_OK)
    
    def retrieve(self,request,store_id,product_id):
        material_quantity = list_material_quantity_service(request,store_id,product_id)
        if not material_quantity:
             return Response({"error":"Material Quantity Not Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(MaterialQuantitySerializer(material_quantity,many=True).data,
                        status=status.HTTP_200_OK)
    
    def destroy(self,request,store_id, material_id,product_id,material_quantity_id):
        material_quantity = delete_material_quantity_service(request,store_id, material_id,product_id,material_quantity_id)
        if not material_quantity:
            return Response({"error":"No Material Quantity Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"response":"Delete Material Quantity Successfully"},
                        status=status.HTTP_200_OK)