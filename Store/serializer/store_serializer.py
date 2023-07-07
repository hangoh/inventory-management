from rest_framework import serializers

from Store.models import Store,Product
from Store.services.store_services import calculate_remaining_product_quantity_service
from Material.models import Material,MaterialQuantity,MaterialStock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","product_uuid","name"]


class StoreSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many = True,  read_only = True)
    class Meta:
        model = Store
        fields = ["store_id","store_uuid","store_name","products"]


class RemainingCapacitySerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
        
    class Meta:
        model = Product
        fields = ["name","product_uuid","quantity"]
    
    def get_quantity(self,obj):
        try:
            material = MaterialQuantity.objects.filter(product = obj)
            material_list = list(material.values())
            material_quantity = []
            material_stock_current_capacity = []
            for m in material_list:
                material_quantity.append(m["quantity"])
                material = Material.objects.get(material_id = m["ingredient_id"])
                material_stock_current_capacity.append(MaterialStock.objects.get(material = material, store = self.context.get("store")).current_capacity)
            quantity = calculate_remaining_product_quantity_service(material_quantity,material_stock_current_capacity)
            return quantity
        except:
            return 0
        

