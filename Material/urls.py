from django.urls import path

from .views import MaterialStockView,MaterialView,MaterialQuantityView

urlpatterns = [
    path('material',MaterialView.as_view({"get":"retrieve","post":"create"}),name='listmaterial'),
    path("material/<uuid:material_uuid>",MaterialView.as_view({"put":"update","delete":"destroy"}),name='material'),
    path("<uuid:store_uuid>/material/stock",MaterialStockView.as_view({"get":"retrieve"}),name='listmaterialstock'),
    path("<uuid:store_uuid>/material/<uuid:material_uuid>/stock",MaterialStockView.as_view({"post":"create"}),name='creatematerialstock'),
    path("<uuid:store_uuid>/material/stock/<uuid:material_stock_uuid>",MaterialStockView.as_view({"put":"update","delete":"destroy"}),name='materialstock'),
    path("<uuid:store_uuid>/product/<uuid:product_uuid>/quantity",MaterialQuantityView.as_view({"get":"retrieve"}),name='listmaterialquantity'),
    path("<uuid:store_uuid>/product/<uuid:product_uuid>/material/<uuid:material_uuid>/quantity",MaterialQuantityView.as_view({"post":"create"}),name='creatematerialquantity'),
    path("<uuid:store_uuid>/product/<uuid:product_uuid>/material/<uuid:material_uuid>/quantity/<uuid:material_quantity_uuid>",MaterialQuantityView.as_view({"put":"update","delete":"destroy"}),name='materialquantity')
]