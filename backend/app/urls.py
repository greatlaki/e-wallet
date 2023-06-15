from django.contrib import admin
from django.urls import path, include

api = [
    path("wallets/", include("wallets.urls")),
]

urlpatterns = [
    path("api/", include(api)),
    path('admin/', admin.site.urls),
]
