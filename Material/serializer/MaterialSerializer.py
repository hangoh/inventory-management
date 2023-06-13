from rest_framework import serializers

from Material.models import Material_Stock,Material

class MaterialStockSerializer(serializers.ModelSerializer):
    capacity_percentage = serializers.SerializerMethodField()
    class Meta:
        model  = Material_Stock
        fields = ["material","max_capacity","current_capacity", "capacity_percentage"]
    
    def get_capacity_percentage(self,obj):
        return "{:.2f}%".format((obj.current_capacity/obj.max_capacity)*100)


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Material
        fields = ["material_id","price","name"]

