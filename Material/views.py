from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from Material.models import Material_Stock
from rest_framework import status
from rest_framework.response import Response
from Services.MaterialService.material_services import *
from Serializer.MaterialSerializer.MaterialSerializer import MaterialStockSerializer,ProductSerializer,MaterialSerializer
# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_products(request,store_id):
    product = list_product_service(request,store_id)
    if not product:
        return Response({"error":"No Product"},
                        status=status.HTTP_404_NOT_FOUND)
    product_serialize = ProductSerializer(product,many=True)
    return Response(product_serialize.data, 
                    status = status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_material(request):
    material = list_material_service()
    if not material:
        return Response({"error":"No Material Found"},
                        status=status.HTTP_404_NOT_FOUND)
    material_serializer = MaterialSerializer(material,many=True)
    return Response(material_serializer.data,
                    status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_material_stock(request,store_id):
    inventory = list_material_stock_service
    if not inventory:
        return Response({"error":"Inventory Empty"},
                        status=status.HTTP_404_NOT_FOUND)
    inventory_serialize = MaterialStockSerializer(inventory, many=True)
    return Response(inventory_serialize.data,
                     status = status.HTTP_200_OK)



