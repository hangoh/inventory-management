from rest_framework import serializers

from Material.models import MaterialStock,Material,MaterialQuantity
from Material.services.material_services import check_for_restock,request_for_restock
from Store.serializer.store_serializer import StoreSerializer,ProductSerializer


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Material
        fields = ["material_id","material_uuid", "price", "name"]


class MaterialStockSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(many = False, read_only = True)
    store = StoreSerializer(many = False, read_only = True)
    capacity_percentage = serializers.SerializerMethodField()
    class Meta:
        model  = MaterialStock
        fields = ["material_stock_uuid","store","material","max_capacity","current_capacity", "capacity_percentage"]
        
    def get_capacity_percentage(self,obj):
        return "{:.2f}%".format((int(obj.current_capacity)/int(obj.max_capacity))*100)


class MaterialQuantitySerializer(serializers.ModelSerializer):
    ingredient = MaterialSerializer(many = False, read_only = True)
    product = ProductSerializer(many = False, read_only = True)
    class Meta:
        model  = MaterialQuantity
        fields = ["material_quantity_uuid", "quantity", "ingredient", "product"]
 


class MaterialRestockSkeleton(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = MaterialStock
    
    def get_price(self,obj):
        price = check_for_restock(obj.material_stock_uuid)
        if price:
           return "{:.2f}".format(price)
        return "-"


class MaterialRestockSerializer(MaterialRestockSkeleton):
    quantity = serializers.SerializerMethodField()
    current_quantity = serializers.SerializerMethodField()

    class Meta:
        model = MaterialStock
        fields = ["material", "current_quantity", "quantity", "price"]
        depth = 1

    def get_current_quantity(self,obj):
        return "{} / {}".format(obj.current_capacity,obj.max_capacity)

    def get_quantity(self,obj):
        return int(obj.max_capacity)-int(obj.current_capacity)

    def get_price(self, obj):
        return super().get_price(obj)
    

class RestockedSerializer(MaterialRestockSkeleton):
    restocked_amount = serializers.SerializerMethodField()

    class Meta:
        model = MaterialStock
        fields = ["material", "price", "restocked_amount"]
        depth = 1
    
    def get_price(self, obj):
        return super().get_price(obj)
        
    def get_restocked_amount(self,obj):
        return request_for_restock(obj.material_stock_uuid)
    
    