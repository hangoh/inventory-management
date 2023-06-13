from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Material.models import Material_Stock,Material
from Material.services.material_services import list_material_service,list_material_stock_service,update_material_service,delete_material_service,update_max_capacity_service,delete_material_stock_service
from Material.serializer.MaterialSerializer import MaterialStockSerializer,MaterialSerializer

# Create your views here.

class MaterialView(ModelViewSet):
    queryset = Material.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MaterialSerializer

    def retrieve(self,request,store_id):
        material = list_material_service(request,store_id)
        if not material:
            return Response({"error":"No Material Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(MaterialSerializer(material,many=True).data,
                        status=status.HTTP_200_OK)
    
    def update(self,request,store_id,material_id):
        material = update_material_service(request,store_id,material_id)
        if not material:
            return Response({"error":"No Material Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(MaterialSerializer(material,many=True).data,
                        status=status.HTTP_200_OK)
    
    def destroy(self,request,store_id,material_id):
        material = delete_material_service(request,store_id,material_id)
        if not material:
            return Response({"error":"No Material Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"response":"Delete Material Successfully"},
                        status=status.HTTP_200_OK)


class MaterialStockView(ModelViewSet):
    queryset = Material_Stock.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MaterialStockSerializer

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
            return Response({"error":"Inventory Empty"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(MaterialStockSerializer(material_stock, many=True).data,
                        status = status.HTTP_200_OK)
    
    def destroy(self, request,store_id,material_stock_id):
        material_stock = delete_material_stock_service(request,store_id,material_stock_id)
        if not material_stock:
            return Response({"error":"No Inventory Found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"response":"Delete Inventory Successfully"},
                        status=status.HTTP_200_OK)



