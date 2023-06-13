from rest_framework import serializers

from Material.models import Store,Product

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["store_id","store_name","products"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name"]