from django.contrib import admin
from django.urls import include, path

api = [
    path("users/", include("users.urls")),
]

urlpatterns = [
    path("api/", include(api)),
    path("admin/", admin.site.urls),
]
