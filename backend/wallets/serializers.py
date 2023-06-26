from django.core.validators import MinValueValidator
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django_extended.constants import TransactionType
from django_extended.serializers import ReadableHiddenField
from rest_framework import serializers
from wallets.models import Transaction, Wallet


class WalletsSerializer(serializers.ModelSerializer):
    owner = ReadableHiddenField(default=serializers.CurrentUserDefault())
    wallet_number = serializers.CharField()
    balance = serializers.DecimalField(
        max_digits=32, decimal_places=2, validators=[MinValueValidator(0.0)]
    )

    class Meta:
        model = Wallet
        fields = (
            "id",
            "owner",
            "name",
            "wallet_number",
            "balance",
        )

    def validate_wallet_number(self, wallet_number):
        wallet_number_exists = Wallet.objects.filter(
            wallet_number__iexact=wallet_number
        ).exists()
        if wallet_number_exists:
            raise serializers.ValidationError("The wallet number already exists")
        return wallet_number


class WalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "id",
            "balance",
        )


class TransactionSerializer(serializers.ModelSerializer):
    wallet_id = serializers.IntegerField()
    # sender_wallet_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=32, decimal_places=2)
    transaction_type = serializers.ChoiceField(
        choices=TransactionType.choices, required=True
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "wallet_id",
            "amount",
            "transaction_type",
        )

    @staticmethod
    def validate_wallet_transaction(transaction_type: str, owner: QuerySet):
        if transaction_type == TransactionType.WITHDRAW and not owner:
            raise serializers.ValidationError(
                {"wallet": "The user must be the owner of the wallet."}
            )
        if transaction_type == TransactionType.TRANSFER and not owner:
            pass

    def validate(self, attrs):
        user = self.context["request"].user
        transaction_type = attrs.get("transaction_type")
        # sender_wallet_id = attrs.get("sender_wallet_id")
        owner = Wallet.objects.filter(owner__id=user.id)
        # sender_wallet = Wallet.objects.get(id=sender_wallet_id)
        if not user.is_superuser:
            self.validate_wallet_transaction(transaction_type, owner)
        return attrs

    def create(self, validated_data):
        wallet_id = validated_data["wallet_id"]
        amount = validated_data["amount"]
        transaction_type = validated_data["transaction_type"]
        direction = get_object_or_404(Wallet, pk=wallet_id)
        match transaction_type:
            case TransactionType.DEPOSIT:
                direction.balance += amount
                direction.save()
            case TransactionType.WITHDRAW:
                direction.balance -= amount
                direction.save()
            case TransactionType.TRANSFER:
                pass
        return super().create(validated_data)
