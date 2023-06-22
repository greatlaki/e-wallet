from django.core.validators import MinValueValidator
from django_extended.serializers import ReadableHiddenField
from rest_framework import serializers
from wallets.models import Wallet


class WalletsSerializer(serializers.ModelSerializer):
    owner = ReadableHiddenField(default=serializers.CurrentUserDefault())
    wallet_number = serializers.CharField()
    amount = serializers.DecimalField(
        max_digits=32, decimal_places=2, validators=[MinValueValidator(0.0)]
    )

    class Meta:
        model = Wallet
        fields = (
            "id",
            "owner",
            "name",
            "wallet_number",
            "amount",
        )

    def validate_wallet_number(self, wallet_number):
        wallet_number_exists = Wallet.objects.filter(
            wallet_number__iexact=wallet_number
        ).exists()
        if wallet_number_exists:
            raise serializers.ValidationError("The wallet number already exists")
        return wallet_number
