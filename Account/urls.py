from django.urls import path
from rest_framework.authtoken import views

from Account.views import UserView,UserCreateView

urlpatterns = [
    path("",UserView.as_view({"get":"retrieve"}), name="user"),
    path("sign-out/",UserView.as_view({"post":"create"}), name="user"),
    path("sign-up/",UserCreateView.as_view({"post":"create"}), name="user_sign_up"),
    path('auth-user/',views.obtain_auth_token, name="authenticate_user"),
]

