from django.shortcuts import redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer

from .models import MaterialStock,Material,MaterialQuantity
from .serializer.MaterialSerializer import MaterialStockSerializer, MaterialSerializer, MaterialQuantitySerializer, MaterialRestockSerializer, RestockedSerializer
from .services.material_services import ( list_material_stock_service, create_material_stock_service ,list_material_quantity_service, 
                                         create_material_quantity_service, return_all_available_material_for_material_quantity_creation, return_all_available_material_for_stock_creation)

from Store.services.store_services import get_store_service, get_product_service
from Account.authentication import CustomSessionAuthentication


# Create your views here.
class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    lookup_field = "material_uuid"
    

class MaterialStockViewSet(ModelViewSet):
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
    

class MaterialQuantityViewSet(ModelViewSet):
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
    

class MaterialRestockViewSet(ModelViewSet):
    queryset = MaterialStock.objects.all()
    serializer_class = MaterialRestockSerializer

    def retrieve(self, request, store_uuid):
        try:
            store = get_store_service(request.user, store_uuid)
            material_stock = MaterialStock.objects.filter(store = store)
            if not material_stock:
                return Response({"error":"No Material Stock Found"},
                            status=status.HTTP_404_NOT_FOUND)
            serialized_objs = MaterialRestockSerializer(material_stock, many = True).data
            material_price_array = [float(obj["price"]) for obj in serialized_objs if obj["price"]!="-"]
            return Response({"total price":"{:.2f}".format(sum(material_price_array)) ,"restock material":serialized_objs}, 
                            status = status.HTTP_200_OK)
        except:
            return Response({"error":"No Material Stock Found"},
                            status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request, store_uuid):
        try:
            store = get_store_service(request.user, store_uuid)
            material_stock = MaterialStock.objects.filter(store = store)
            if not material_stock:
                return Response({"error":"Fail To Restock"},
                            status=status.HTTP_400_BAD_REQUEST)
            serialized_objs = RestockedSerializer(material_stock,many = True).data
            material_price_array = [float(obj["price"]) for obj in serialized_objs if obj["price"]!="-"]
            return Response({"total price":"{:.2f}".format(sum(material_price_array)) ,"restock material":serialized_objs}, 
                            status = status.HTTP_200_OK)
        except:
             return Response({"error":"Fail To Restock"},
                            status=status.HTTP_400_BAD_REQUEST)

"""
Template View
"""

class CreateMaterialTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "material_template/creatematerial.html"

    def retrieve(self, request):
        serializer = MaterialSerializer()
        return Response({"serializer": serializer})
    
    def create(self, request):
        serializer = MaterialSerializer()
        try:
            serializer = MaterialSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({'serializer': serializer, 'error': "Failed to create material"})
            material = Material.objects.create(name = serializer.data["name"], price = serializer.data["price"])
            material.save()
            return redirect('liststorestemplate')
        except:
            return Response({'serializer': serializer, 'error': "Failed to create material"})


class EditMaterialTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "material_template/materialedit.html"

    def retrieve(self,request):
        material = Material.objects.all()
        return Response({"materials":material})
    

class MaterialPUTTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    lookup_field = "material_uuid"

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except:
            return Response({"error":"Failed To Update Material"})

class MaterialStockTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "material_template/materialstock.html"

    def retrieve(self, request, store_uuid):
        store = get_store_service(request.user, store_uuid)
        material_stock = list_material_stock_service(request, store_uuid)
        if material_stock:
            material_stock = MaterialStockSerializer(material_stock, many = True).data
        return Response({"store":store, "material_stock": material_stock})
    
 
class CreateMaterialStockTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "material_template/creatematerialstock.html"

    def retrieve(self, request, store_uuid):
        material = return_all_available_material_for_stock_creation(request, store_uuid)
        return Response({"store_uuid":store_uuid, "material":material})
    
    def create(self, request, store_uuid):
        material_uuid = request.data["material_uuid"]
        material = return_all_available_material_for_stock_creation(request, store_uuid)
        material_stock = create_material_stock_service(request, store_uuid, material_uuid) 
        if not material_stock:
             return Response({"error":"Fail To Create Material Stock. Check if you have already created a stock for this material", "store_uuid":store_uuid, "material":material})
        return redirect("materialstocktemplate", store_uuid=store_uuid)
    

class MaterialStockPUTAndDELETETemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    queryset = MaterialStock.objects.all()
    serializer_class = MaterialStockSerializer
    lookup_field = "material_stock_uuid"
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except:
            return Response({"error":"Invalid Max Capacity"})


class RestockMaterialStockTemplateView(ModelViewSet):
    authentication_classes=[CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "material_template/restockmaterial.html"

    def retrieve(self, request, store_uuid):
        try:
            store = get_store_service(request.user, store_uuid)
            material_stock = MaterialStock.objects.filter(store = store)
            if not material_stock:
                return Response({"error":"No Material Stock Found", "store_uuid":store_uuid})
            serialized_objs = MaterialRestockSerializer(material_stock, many = True).data
            material_price_array = [float(obj["price"]) for obj in serialized_objs if obj["price"]!="-"]
            return Response({"total_price":"{:.2f}".format(sum(material_price_array)) ,"restock_material":serialized_objs, "store_uuid":store_uuid})
        except:
            return Response({"error":"No Material Stock Found", "store_uuid":store_uuid})
        
    def create(self, request, store_uuid):
        try:
            store = get_store_service(request.user, store_uuid)
            material_stock = MaterialStock.objects.filter(store = store)
            if not material_stock:
                return Response({"error":"Fail To Restock", "store_uuid":store_uuid})
            serialized_objs = RestockedSerializer(material_stock,many = True).data
            material_price_array = [float(obj["price"]) for obj in serialized_objs if obj["price"]!="-"]
            return Response({"total_price":"{:.2f}".format(sum(material_price_array)) ,"restock_material":serialized_objs, "store_uuid":store_uuid})
        except:
             return Response({"error":"Fail To Restock", "store_uuid":store_uuid})
        

class MaterialQuantityPUTAndDELETETemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    queryset = MaterialQuantity.objects.all()
    serializer_class = MaterialQuantitySerializer
    lookup_field = "material_quantity_uuid"

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except:
            return Response({"error":"quantity should be an integer greater than or equal to 1"}, status = status.HTTP_400_BAD_REQUEST)
        

class CreateMaterialQuantityTemplateViewSet(ModelViewSet):
    authentication_classes=[CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "material_template/creatematerialquantity.html"
    
    def retrieve(self, request, store_uuid, product_uuid):
        material = return_all_available_material_for_material_quantity_creation(request, store_uuid, product_uuid)
        product = get_product_service(request, store_uuid, product_uuid)
        return Response({"materials":material, "store_uuid":store_uuid, "product":product})
    
    def create(self, request, store_uuid, product_uuid):
        print(request.data)
        material = return_all_available_material_for_material_quantity_creation(request, store_uuid, product_uuid)
        product = get_product_service(request, store_uuid, product_uuid)
        material_quantity = create_material_quantity_service(request, store_uuid, request.data["material_uuid"], product_uuid)
        if material_quantity:
            return redirect("productedittemplate", store_uuid = store_uuid, product_uuid = product_uuid)
        return Response({"materials":material, "store_uuid":store_uuid, "product":product, "error":"Failed To Added Material Quantity For {}".format(product.name)})