import json
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import JSONParser

from .models import Product,Store
from .serializer.store_serializer import StoreSerializer,ProductSerializer,RemainingCapacitySerializer
from .services.store_services import (get_stores_service, get_store_service, 
list_product_service, create_product_service, create_store_service,
product_sales_services, check_material_quantity_duplicate, get_product_service)

from Account.authentication import CustomSessionAuthentication
from Material.models import MaterialStock
from Material.serializer.MaterialSerializer import MaterialStockSerializer
from Material.services.material_services import list_material_stock_service, create_product_and_material_quantity_service, list_material_quantity_service

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

    def create(self, request, store_uuid):
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
    

"""
Template Views
"""

class StoreTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    lookup_field = "store_uuid"
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'store_template/stores.html'

    def retrieve(self,request,store_uuid=None):
        error={}
        if not store_uuid:
            store = get_stores_service(request.user)
            if not store:
                error["error"] = "This User Didn't Have A Store Yet"
                return Response(error)
            serializedStore = StoreSerializer(store, many=True)
            return Response({"stores":serializedStore.data})
        else:
            store = get_store_service(request.user,store_uuid)
            if not store:
                error["error"] = "Store Not Found"
                return Response(error)
            serializedStore = StoreSerializer(store, many=False)
            return Response({"store":serializedStore.data})
    

class CreateStoreTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "store_template/createstore.html"

    def retrieve(self, request):
        serializer = StoreSerializer()
        return Response({"serializer":serializer})
    
    def create(self, request):
        serializer = StoreSerializer()
        store = create_store_service(request)
        if not store:
            return Response({"serializer":serializer, "error":"Fail To Create store"})
        return redirect("liststorestemplate")
    
class StorePutAndDeleteTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    queryset = Store.objects.all()
    lookup_field = "store_uuid"
    serializer_class = StoreSerializer


class CreateProductTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product_template/createproduct.html"

    def retrieve(self, request, store_uuid):
        material_stock = list_material_stock_service(request, store_uuid)
        material = []
        if material_stock:
            material = [m_s.material for m_s in material_stock]
        return Response({"store_uuid":store_uuid, "material":material})

    def create(self, request, store_uuid):
        material_stock = list_material_stock_service(request, store_uuid)
        material = []
        if material_stock:
            material = [m_s.material for m_s in material_stock]
        #get the material_uuid and quantity of the material into and array and check if identical uuid is provided before proceeding.
        request_material_quantity_array = [value for value in request.data.keys() if value!='csrfmiddlewaretoken' and value!="name"]
        duplicate_material_quantity = check_material_quantity_duplicate(request, request_material_quantity_array)
        if duplicate_material_quantity:
            return Response({"error":"material of the same type is chosen more than once", "store_uuid":store_uuid, "material":material})
        product_material_quantity_created = create_product_and_material_quantity_service(request, store_uuid, request_material_quantity_array)
        if product_material_quantity_created:
            return redirect("getstoretemplate", store_uuid = store_uuid)
        return Response({"error":"fail to create product", "store_uuid":store_uuid, "material":material})


class ProductEditTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product_template/productedit.html"
    queryset = Product.objects.all()
    lookup_field = "product_uuid"
    serializer_class = ProductSerializer
    
    def retrieve(self,request,store_uuid,product_uuid):
        store = get_store_service(request.user,store_uuid)
        error = "Store Not Found"
        if store:
            product = get_product_service(request,store_uuid,product_uuid)
            if product:
                material_quantity = list_material_quantity_service(request, store_uuid, product_uuid)
                return Response({"store_uuid":store_uuid, "product":product, "material_quantity":material_quantity})
            error = "Product Not Found"
        return Response({"error":error, "store_uuid":store_uuid}) 
    

class ProductPutDeleteTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    queryset = Product.objects.all()
    lookup_field = "product_uuid"
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs): 
        try:
            return super().update(request, *args, **kwargs)
        except:
            return Response({"error":"This Field Should Not Be Blank"}, status = status.HTTP_400_BAD_REQUEST)


class ProductCapacityTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product_template/productcapacity.html"

    def retrieve(self, request, store_uuid):
        product = list_product_service(request,store_uuid)
        store = get_store_service(request.user,store_uuid )
        if not product:
            return Response({"error":"No Product", "store_uuid":store_uuid})
        return Response({"product":RemainingCapacitySerializer(product, many = True, context={'store': store}).data, "store_uuid":store_uuid })
    

class SalesTemplateViewSet(ModelViewSet):
    authentication_classes = [CustomSessionAuthentication]

    def create(self,request,store_uuid):
        response = product_sales_services(request = request, store_uuid = store_uuid)
        if response["sale"] == []:
            return Response({"error":response["error"], "store_uuid":store_uuid})
        return Response({"sale":response["sale"], "error":response["error"], "store_uuid":store_uuid})