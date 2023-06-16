from django.urls import path

from .views import StoreView,ProductView

urlpatterns = [
    path('',StoreView.as_view({"get":"retrieve", "post":"create"}), name="liststores"),
    path('<int:store_uuid>',StoreView.as_view({"get":"retrieve", "put":"update", "delete":"destroy"}),name="store"),
    path("<int:store_uuid>/products",ProductView.as_view({"get":"retrieve", "post":"create"}),name='listproducts'),
    path("<int:store_uuid>/products/<int:product_uuid>",ProductView.as_view({"put":"update", "delete":"destroy"}),name='product'),
]