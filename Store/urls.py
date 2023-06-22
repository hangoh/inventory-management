from django.urls import path

from .views import StoreViewSet, ProductViewSet, ProductCapacityViewSet, SalesViewSet

urlpatterns = [
    path('',StoreViewSet.as_view({"get":"retrieve", "post":"create"}), name="liststores"),
    path('<uuid:store_uuid>',StoreViewSet.as_view({"get":"retrieve", "put":"update", "delete":"destroy"}),name="store"),
    path("<uuid:store_uuid>/products",ProductViewSet.as_view({"get":"list", "post":"create"}),name='listproducts'),
    path("<uuid:store_uuid>/products/sales",SalesViewSet.as_view({"post":"create"}),name='productssales'),
    path("<uuid:store_uuid>/products/products-capacity",ProductCapacityViewSet.as_view({"get":"retrieve"}),name='productscapacity'),
    path("<uuid:store_uuid>/products/<uuid:product_uuid>",ProductViewSet.as_view({"put":"update", "delete":"destroy"}),name='product'),
]