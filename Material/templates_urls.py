from django.urls import path

from Material.views import (CreateMaterialTemplateViewSet, EditMaterialTemplateViewSet, MaterialStockTemplateViewSet, CreateMaterialStockTemplateViewSet,
                            RestockMaterialStockTemplateView, MaterialStockPUTAndDELETETemplateViewSet, MaterialQuantityPUTAndDELETETemplateViewSet,
                            CreateMaterialQuantityTemplateViewSet, MaterialPUTTemplateViewSet)

urlpatterns = [
   path("material", CreateMaterialTemplateViewSet.as_view({"get":"retrieve","post":"create"}), name = "creatematerialtemplate"),
   path("material/edit", EditMaterialTemplateViewSet.as_view({"get":"retrieve"}), name = "materialedittemplate"),
   path("material/<uuid:material_uuid>/edit", MaterialPUTTemplateViewSet.as_view({"put":"update"}), name = "materialputtemplate"),
   path("<uuid:store_uuid>/material/stock", MaterialStockTemplateViewSet.as_view({"get":"retrieve"}), name = "materialstocktemplate"),
   path("<uuid:store_uuid>/material/stock/create", CreateMaterialStockTemplateViewSet.as_view({"get":"retrieve","post":"create"}), name = "creatematerialstocktemplate"),
   path("<uuid:store_uuid>/material/stock/restock", RestockMaterialStockTemplateView.as_view({"get":"retrieve","post":"create"}), name = "restockmaterialstocktemplate"),
   path("<uuid:store_uuid>/material/stock/<uuid:material_stock_uuid>/edit-delete", MaterialStockPUTAndDELETETemplateViewSet.as_view({"put":"update", "delete":"destroy"}), name = "materialstockputdeletetemplate"),
   path("<uuid:store_uuid>/material/product/<uuid:product_uuid>/quantity/create", CreateMaterialQuantityTemplateViewSet.as_view({"get":"retrieve","post":"create"}), name = "creatematerialquantitytemplate"),
   path("<uuid:store_uuid>/material/quantity/<uuid:material_quantity_uuid>/edit-delete", MaterialQuantityPUTAndDELETETemplateViewSet.as_view({"put":"update", "delete":"destroy"}), name = "materialquantityputdeletetemplate")
]