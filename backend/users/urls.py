from django.urls import path
from users.views import RegisterApiView, LoginApiView, LogoutAPIView

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="registration"),
    path("login/", LoginApiView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
