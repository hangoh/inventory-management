from django.urls import path

from .views import (StoreTemplateViewSet, CreateStoreTemplateViewSet, StorePutAndDeleteTemplateViewSet, CreateProductTemplateViewSet, 
                    ProductCapacityTemplateViewSet, SalesTemplateViewSet, ProductEditTemplateViewSet, ProductPutDeleteTemplateViewSet)

urlpatterns = [
    path('',StoreTemplateViewSet.as_view({"get":"retrieve"}), name="liststorestemplate"),
    path('<uuid:store_uuid>',StoreTemplateViewSet.as_view({"get":"retrieve"}),name="getstoretemplate"),
    path('<uuid:store_uuid>/edit-delete',StorePutAndDeleteTemplateViewSet.as_view({"put":"update","delete":"destroy"}), name="storeputdeletetemplate"),
    path('create',CreateStoreTemplateViewSet.as_view({"get":"retrieve","post":"create"}), name="createstoretemplate"),
    path('<uuid:store_uuid>/product/create',CreateProductTemplateViewSet.as_view({"get":"retrieve","post":"create"}), name="createproducttemplate"),
    path('<uuid:store_uuid>/product/capacity',ProductCapacityTemplateViewSet.as_view({"get":"retrieve"}), name="productcapacitytemplate"),
    path('<uuid:store_uuid>/product/sales',SalesTemplateViewSet.as_view({"post":"create"}), name="salestemplate"),
    path('<uuid:store_uuid>/product/<uuid:product_uuid>',ProductEditTemplateViewSet.as_view({"get":"retrieve"}), name="productedittemplate"),
    path('<uuid:store_uuid>/product/<uuid:product_uuid>/edit-delete', ProductPutDeleteTemplateViewSet.as_view({"put":"update","delete":"destroy"}), name="productputdeletetemplate")
]