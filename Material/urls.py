from django.urls import path

from Material.views import MaterialStockView,MaterialView

urlpatterns = [
    path("<int:store_id>/material",MaterialView.as_view({"get":"retrieve"}),name='list_material'),
    path("<int:store_id>/material/<int:material_id>",MaterialView.as_view({"put":"update","delete":"destroy"}),name='material'),
    path("<int:store_id>/material/stock",MaterialStockView.as_view({"get":"retrieve"}),name='list_material_stock'),
    path("<int:store_id>/material/stock/<int:material_stock_id>",MaterialStockView.as_view({"put":"update","delete":"destroy"}),name='material_stock')
]