from json import dumps

from django.db.models import Q
from django_extended.constants import RequestMethods
from kafka import KafkaProducer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from wallets.models import Transaction, Wallet
from wallets.serializers.transaction_serialziers import (
    TransactionListCreateSerializer,
    TransactionRetrieveUpdateSerializer,
)
from wallets.serializers.wallet_serializers import (
    WalletsBalanceSerializer,
    WalletsListCreateSerializer,
    WalletsRetrieveUpdateDestroySerializer,
)


class WalletsListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletsListCreateSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Wallet.objects.all()
        return Wallet.objects.filter(owner=user.pk).order_by("id")


class WalletsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletsRetrieveUpdateDestroySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Wallet.objects.all()
        return Wallet.objects.filter(owner=user.pk)


class WalletsBalanceAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletsBalanceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Wallet.objects.all()
        return Wallet.objects.filter(owner=user.pk)


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionListCreateSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_admin:
            return Transaction.objects.all()
        return Transaction.objects.filter(Q(wallet__owner_id=user.pk) | Q(receiver__id=user.pk))

    def post(self, request, *args, **kwargs):
        create_transaction = self.create(request, *args, **kwargs)
        producer = KafkaProducer(
            bootstrap_servers=["kafka:29092"],
            api_version=(0, 11, 5),
            value_serializer=lambda x: dumps(x).encode("utf-8"),
        )
        producer.send("transactions_create", value=create_transaction)


class TransactionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TransactionRetrieveUpdateSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_admin:
            return Transaction.objects.all()
        return Transaction.objects.filter(wallet__owner_id=user.pk)

    def get_permissions(self):
        if self.request.method in [RequestMethods.PATCH]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
