from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from wallets.models import Transaction, Wallet
from wallets.serializers import (
    TransactionSerializer,
    WalletBalanceSerializer,
    WalletsSerializer,
)


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


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(
            Q(wallet__owner_id=user.pk) | Q(receiver__id=user.pk)
        )


class TransactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(wallet__owner_id=user.pk)
