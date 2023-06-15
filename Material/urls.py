from django.urls import path

from Material.views import MaterialStockView,MaterialView,MaterialQuantityView

urlpatterns = [
    path('material',MaterialView.as_view({"get":"retrieve","post":"create"}),name='list_material'),
    path("material/<int:material_id>",MaterialView.as_view({"put":"update","delete":"destroy"}),name='material'),
    path("<int:store_id>/material/stock",MaterialStockView.as_view({"get":"retrieve"}),name='list_material_stock'),
    path("<int:store_id>/material/<int:material_id>/stock",MaterialStockView.as_view({"post":"create"}),name='create_material_stock'),
    path("<int:store_id>/material/stock/<int:material_stock_id>",MaterialStockView.as_view({"put":"update","delete":"destroy"}),name='material_stock'),
    path("<int:store_id>/product/<int:product_id>/quantity",MaterialQuantityView.as_view({"get":"retrieve"}),name='list_material_quantity'),
    path("<int:store_id>/product/<int:product_id>/material/<int:material_id>/quantity",MaterialQuantityView.as_view({"post":"create"}),name='create_material_quantity'),
    path("<int:store_id>/product/<int:product_id>/material/<int:material_id>/quantity/<int:material_quantity_id>",MaterialQuantityView.as_view({"put":"update","delete":"destroy"}),name='material_quantity')
]