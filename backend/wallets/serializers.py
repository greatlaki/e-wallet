from django.core.validators import MinValueValidator
from django_extended.constants import TransactionType
from django_extended.serializers import ReadableHiddenField
from rest_framework import serializers
from users.models import User
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
    receiver_wallet_id = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=32, decimal_places=2)
    transaction_type = serializers.ChoiceField(
        choices=TransactionType.choices, required=True
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "wallet_id",
            "receiver_wallet_id",
            "amount",
            "transaction_type",
        )

    @staticmethod
    def validate_wallet_existence(wallet_id: int):
        if wallet_id is None:
            return
        if not Wallet.objects.filter(id=wallet_id).exists():
            raise serializers.ValidationError(
                {"wallet_id": "The wallet does not exist."}
            )

    @staticmethod
    def validate_wallet_transaction(user: User, wallet_id: int, transaction_type: str):
        if (
            # transaction_type == TransactionType.WITHDRAW
            wallet_id
            not in user.get_wallets_ids()
        ):
            raise serializers.ValidationError(
                {"wallet": "The user must be the owner of the wallet."}
            )
        if transaction_type == TransactionType.TRANSFER:
            pass

    def validate(self, attrs):
        user = self.context["request"].user
        wallet_id = attrs.get("wallet_id")
        transaction_type = attrs.get("transaction_type")
        receiver_wallet_id = attrs.get("receiver_wallet_id")
        self.validate_wallet_existence(wallet_id)
        self.validate_wallet_existence(receiver_wallet_id)
        if not user.is_superuser:
            self.validate_wallet_transaction(user, wallet_id, transaction_type)
        return attrs

    def create(self, validated_data):
        direction = validated_data["wallet_id"]
        amount = validated_data["amount"]
        transaction_type = validated_data["transaction_type"]
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
