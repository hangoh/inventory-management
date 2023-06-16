from rest_framework import serializers

from Store.models import Store,Product
from Store.services.store_services import calculate_remaining_product_quantity
from Material.models import MaterialStock,MaterialQuantity,Material



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["uuid","name"]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["uuid","store_name","products"]
        depth = 1


class RemainingCapacitySerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
        
    class Meta:
        model = Product
        fields = ["name","uuid","quantity"]

    def get_quantity(self,obj):
        try:
            material = MaterialQuantity.objects.filter(product = obj)
            material_list = list(material.values())
            material_quantity = []
            material_stock_current_capacity = []
            for m in material_list:
                material_quantity.append(m["quantity"])
                material = Material.objects.get(material_id = m["ingredient_id"])
                material_stock_current_capacity.append(MaterialStock.objects.get(material=material).current_capacity)
            quantity = calculate_remaining_product_quantity(material_quantity,material_stock_current_capacity)
            return quantity
        except:
            return 0
    