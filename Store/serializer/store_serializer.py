from rest_framework import serializers

from Store.models import Store,Product
from Store.services.store_services import get_quantity


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","product_uuid","name"]


class StoreSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many = True)
    class Meta:
        model = Store
        fields = ["store_id","store_uuid","store_name","products"]


class RemainingCapacitySerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
        
    class Meta:
        model = Product
        fields = ["name","product_uuid","quantity"]

    def get_quantity(self,obj):
        return get_quantity(obj)
        

