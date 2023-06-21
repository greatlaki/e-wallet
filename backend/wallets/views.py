from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from wallets.models import Wallet
from wallets.serializers import WalletsListCreateSerializer


class WalletsListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletsListCreateSerializer
    queryset = Wallet.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Wallet.objects.all()
        return Wallet.objects.filter(owner=user.pk).order_by("name")
