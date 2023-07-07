from django.urls import path

from Account.views import ObtainAuthTokenTemplateView,LogOutTemplateViewSet,RegisterTemplateViewSet

urlpatterns = [
   path("",ObtainAuthTokenTemplateView.as_view(),name="authenticateusertemplate"),
   path("logout",LogOutTemplateViewSet.as_view({"delete":"destroy"}),name="logouttemplate"),
   path("register",RegisterTemplateViewSet.as_view({"get":"retrieve", "post":"create"}),name="registertemplate"),
]

