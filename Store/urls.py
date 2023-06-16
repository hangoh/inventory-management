from django.urls import path

from .views import StoreView,ProductView,ProductCapacityView

urlpatterns = [
    path('',StoreView.as_view({"get":"retrieve", "post":"create"}), name="liststores"),
    path('<uuid:store_uuid>',StoreView.as_view({"get":"retrieve", "put":"update", "delete":"destroy"}),name="store"),
    path("<uuid:store_uuid>/products",ProductView.as_view({"get":"retrieve", "post":"create"}),name='listproducts'),
    path("<uuid:store_uuid>/products/products-capacity",ProductCapacityView.as_view({"get":"retrieve"}),name='productscapacity'),
    path("<uuid:store_uuid>/products/<uuid:product_uuid>",ProductView.as_view({"put":"update", "delete":"destroy"}),name='product'),
]