from rest_framework import serializers

from Material.models import MaterialStock,Material,MaterialQuantity


class MaterialStockSerializer(serializers.ModelSerializer):
    capacity_percentage = serializers.SerializerMethodField()
    class Meta:
        model  = MaterialStock
        fields = ["material","max_capacity","current_capacity", "capacity_percentage"]
        depth = 1
    
    def get_capacity_percentage(self,obj):
        return "{:.2f}%".format((int(obj.current_capacity)/int(obj.max_capacity))*100)


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Material
        fields = ["material_id","price","name"]


class MaterialQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = MaterialQuantity
        fields = ["id","quantity","ingredient","product"]
        depth = 1

