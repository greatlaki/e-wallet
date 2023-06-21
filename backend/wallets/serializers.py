from django_extended.serializers import ReadableHiddenField
from rest_framework import serializers
from wallets.models import Wallet


class WalletsListCreateSerializer(serializers.ModelSerializer):
    owner = ReadableHiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Wallet
        fields = (
            "id",
            "owner",
            "name",
            "wallet_number",
            "amount",
        )
