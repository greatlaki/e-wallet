from django.urls import path
from wallets.views import WalletsListCreateAPIView

urlpatterns = [
    path("", WalletsListCreateAPIView.as_view(), name="list-create-wallets"),
]
