from django.urls import path
from wallets.views import WalletsListCreateAPIView, WalletsRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", WalletsListCreateAPIView.as_view(), name="list-create-wallets"),
    path(
        "<int:pk>/",
        WalletsRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy-wallets",
    ),
]
