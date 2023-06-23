from django.urls import path

from .views import UserViewSet,UserCreateViewSet,ObtainAuthTokenView

urlpatterns = [
    path("",UserViewSet.as_view({"get":"retrieve"}), name="user"),
    path("sign-out",UserViewSet.as_view({"post":"create"}), name="usersignout"),
    path("sign-up",UserCreateViewSet.as_view({"post":"create"}), name="usersignup"),
    path("auth-user",ObtainAuthTokenView.as_view(), name="authenticateuser"),
]

