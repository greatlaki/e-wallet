from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from wallets.models import Wallet
from wallets.serializers import WalletBalanceSerializer, WalletsSerializer


class WalletsListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Wallet.objects.all()
        return Wallet.objects.filter(owner=user.pk).order_by("name")


class WalletsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Wallet.objects.all()
        return Wallet.objects.filter(owner=user.pk)


class WalletsBalanceAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletBalanceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Wallet.objects.all()
        return Wallet.objects.filter(owner=user.pk)
