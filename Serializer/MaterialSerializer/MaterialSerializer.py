from rest_framework import serializers
from Material.models import Store,Material_Stock,Product,Material

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["store_id","store_name","products"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name"]

class MaterialStockSerializer(serializers.ModelSerializer):
    capacity_percentage = serializers.DecimalField(max_digits=3,decimal_places=2)
    class Meta:
        model  = Material_Stock
        fields = ["material","max_capacity","current_capacity", "capacity_percentage"]
    
    def get_capacity_percentage(self,obj):
        return obj.current_capacity/obj.max_capacity

class StoreMaterialSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    material_name = serializers.CharField()
    material_price = serializers.DecimalField(decimal_places=2,max_digits=8)
    class Meta:
        model  = Material_Stock
        fields = ["id","material_name","material_price"]

    def get_id(self,obj):
        return Material.objects.get(obj.material).material_id
    
    def get_material_name(self,obj):
        return Material.objects.get(obj.material).name
    
    def get_material_price(self,obj):
        return Material.objects.get(obj.material).price
    
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Material
        fields = ["material_id","price","name"]

