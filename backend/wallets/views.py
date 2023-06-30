from django.db.models import Q
from django_extended.constants import RequestMethods
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from wallets.models import Transaction, Wallet
from wallets.serializers.transaction_serialziers import (
    TransactionListCreateSerializer,
    TransactionRetrieveUpdateDestroySerializer,
)
from wallets.serializers.wallet_serializers import (
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
    serializer_class = TransactionListCreateSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(
            Q(wallet__owner_id=user.pk) | Q(receiver__id=user.pk)
        )


class TransactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionRetrieveUpdateDestroySerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(wallet__owner_id=user.pk)

    def get_permissions(self):
        if self.request.method in [RequestMethods.PATCH, RequestMethods.DELETE]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
