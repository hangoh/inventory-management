from rest_framework import serializers

from Store.models import Store,Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["uuid","name"]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["uuid","store_name","products"]
        depth = 1

