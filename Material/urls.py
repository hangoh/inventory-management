from django.urls import path

from .views import MaterialStockViewSet,MaterialViewSet,MaterialQuantityViewSet,MaterialRestockViewSet

urlpatterns = [
    path('material',MaterialViewSet.as_view({"get":"list","post":"create"}),name='listmaterial'),
    path("material/<uuid:material_uuid>",MaterialViewSet.as_view({"put":"update","delete":"destroy"}),name='material'),
    path("<uuid:store_uuid>/material/stock",MaterialStockViewSet.as_view({"get":"retrieve"}),name='listmaterialstock'),
    path("<uuid:store_uuid>/material/<uuid:material_uuid>/stock",MaterialStockViewSet.as_view({"post":"create"}),name='creatematerialstock'),
    path("<uuid:store_uuid>/material/stock/<uuid:material_stock_uuid>",MaterialStockViewSet.as_view({"put":"update","delete":"destroy"}),name='materialstock'),
    path("<uuid:store_uuid>/material/stock/restock",MaterialRestockViewSet.as_view({"get":"retrieve","post":"create"}),name='materialrestock'),
    path("<uuid:store_uuid>/product/<uuid:product_uuid>/quantity",MaterialQuantityViewSet.as_view({"get":"retrieve"}),name='listmaterialquantity'),
    path("<uuid:store_uuid>/product/<uuid:product_uuid>/material/<uuid:material_uuid>/quantity",MaterialQuantityViewSet.as_view({"post":"create"}),name='creatematerialquantity'),
    path("<uuid:store_uuid>/product/<uuid:product_uuid>/material/<uuid:material_uuid>/quantity/<uuid:material_quantity_uuid>",MaterialQuantityViewSet.as_view({"put":"update","delete":"destroy"}),name='materialquantity')
]