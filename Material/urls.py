from django.urls import path

from .views import MaterialStockView,MaterialView,MaterialQuantityView

urlpatterns = [
    path('material',MaterialView.as_view({"get":"retrieve","post":"create"}),name='listmaterial'),
    path("material/<int:material_uuid>",MaterialView.as_view({"put":"update","delete":"destroy"}),name='material'),
    path("<int:store_uuid>/material/stock",MaterialStockView.as_view({"get":"retrieve"}),name='listmaterialstock'),
    path("<int:store_uuid>/material/<int:material_uuid>/stock",MaterialStockView.as_view({"post":"create"}),name='creatematerialstock'),
    path("<int:store_uuid>/material/stock/<int:material_stock_uuid>",MaterialStockView.as_view({"put":"update","delete":"destroy"}),name='materialstock'),
    path("<int:store_uuid>/product/<int:product_uuid>/quantity",MaterialQuantityView.as_view({"get":"retrieve"}),name='listmaterialquantity'),
    path("<int:store_uuid>/product/<int:product_uuid>/material/<int:material_uuid>/quantity",MaterialQuantityView.as_view({"post":"create"}),name='creatematerialquantity'),
    path("<int:store_uuid>/product/<int:product_uuid>/material/<int:material_uuid>/quantity/<int:material_quantity_uuid>",MaterialQuantityView.as_view({"put":"update","delete":"destroy"}),name='materialquantity')
]