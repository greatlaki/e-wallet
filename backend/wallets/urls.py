from django.urls import path
from wallets.views import (
    WalletsBalanceAPIView,
    WalletsListCreateAPIView,
    WalletsRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", WalletsListCreateAPIView.as_view(), name="list-create-wallets"),
    path(
        "<int:pk>/",
        WalletsRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy-wallet",
    ),
    path(
        "<int:pk>/balance/",
        WalletsBalanceAPIView.as_view(),
        name="retrieve-wallet-balance",
    ),
]
