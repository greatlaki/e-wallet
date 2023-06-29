from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import transaction
from django_extended.constants import RequestMethods, TransactionType
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


class TransactionBaseSerializer(serializers.ModelSerializer):
    def validate_wallet_id(self, wallet_id: int):
        wallet_exists = Wallet.objects.filter(id=wallet_id).exists()
        if not wallet_exists:
            raise serializers.ValidationError(
                {"wallet_id": "The wallet does not exist."}
            )
        return wallet_id

    def validate_receiver_id(self, receiver_id: int):
        if receiver_id is None:
            return
        wallet_exists = Wallet.objects.filter(id=receiver_id).exists()
        if not wallet_exists:
            raise serializers.ValidationError(
                {"receiver_id": "The wallet does not exist."}
            )
        return receiver_id

    @staticmethod
    def validate_wallet_transaction(
        user: User,
        wallet_id: int,
        receiver_id: int,
        transaction_type: str,
        request_method: str,
    ):
        if not transaction_type:
            return
        if (
            (
                transaction_type == TransactionType.WITHDRAW
                or transaction_type == TransactionType.TRANSFER
            )
            and not user.is_superuser
            and wallet_id not in user.get_wallets_ids()
        ):
            raise serializers.ValidationError(
                {"wallet_id": "The user must be the owner of the wallet."}
            )
        if transaction_type == TransactionType.TRANSFER and not receiver_id:
            raise serializers.ValidationError(
                {"receiver_id": "The wallet of the recipient must be entered."}
            )
        if receiver_id and transaction_type != TransactionType.TRANSFER:
            raise serializers.ValidationError(
                {
                    "receiver_id": "The recipient can only be specified if the transaction type is transfer"
                }
            )
        if (
            request_method == RequestMethods.PATCH
            and transaction_type != TransactionType.CANCELLATION
        ):
            raise serializers.ValidationError(
                {
                    "transaction_type": "The user cannot change transaction types. The transaction can only be canceled by the administrator."
                }
            )

    def validate(self, attrs):
        user = self.context["request"].user
        request_method = self.context["request"].method
        wallet_id = attrs.get("wallet_id")
        receiver_id = attrs.get("receiver_id")
        transaction_type = attrs.get("transaction_type")
        self.validate_wallet_transaction(
            user, wallet_id, receiver_id, transaction_type, request_method
        )
        return attrs


class TransactionListCreateSerializer(TransactionBaseSerializer):
    wallet_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(
        max_digits=32, decimal_places=2, validators=[MinValueValidator(0.0)]
    )
    transaction_type = serializers.ChoiceField(
        choices=TransactionType.choices, required=True
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "wallet_id",
            "receiver_id",
            "amount",
            "transaction_type",
        )

    def create(self, validated_data):
        wallet_id = validated_data.get("wallet_id")
        receiver_id = validated_data.get("receiver_id")
        amount = validated_data.get("amount")
        transaction_type = validated_data.get("transaction_type")
        wallet = Wallet.objects.get(id=wallet_id)
        match transaction_type:
            case TransactionType.DEPOSIT:
                wallet.balance += amount
            case TransactionType.WITHDRAW:
                wallet.balance -= amount
            case TransactionType.TRANSFER:
                if receiver_id is None:
                    return
                with transaction.atomic():
                    receiver_wallet = Wallet.objects.get(id=receiver_id)
                    wallet.balance -= amount
                    receiver_wallet.balance += amount
                    receiver_wallet.save()
        wallet.save()
        return super().create(validated_data)


class TransactionRetrieveUpdateDestroySerializer(TransactionBaseSerializer):
    wallet_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(
        max_digits=32, decimal_places=2, validators=[MinValueValidator(0.0)]
    )
    transaction_type = serializers.ChoiceField(
        choices=TransactionType.choices, required=False
    )

    class Meta:
        model = Transaction
        fields = (
            "id",
            "wallet_id",
            "receiver_id",
            "amount",
            "transaction_type",
        )

    def validate_amount(self, amount: Decimal):
        if amount == Decimal("0.0"):
            raise serializers.ValidationError(
                {
                    "amount": "The amount should be more than '0', otherwise cancel the transaction"
                }
            )
        return amount

    def update(self, instance, validated_data):
        wallet_id = instance.wallet.id
        receiver_id = None
        if instance.receiver:
            receiver_id = instance.receiver.id
        amount = validated_data.get("amount", instance.amount)
        transaction_type = instance.transaction_type
        cancellation_type = validated_data.get("transaction_type")
        wallet = Wallet.objects.get(id=wallet_id)
        match transaction_type:
            case TransactionType.DEPOSIT:
                wallet.balance += amount
            case TransactionType.WITHDRAW:
                wallet.balance -= amount
            case TransactionType.TRANSFER:
                if receiver_id is None:
                    return
                with transaction.atomic():
                    receiver_wallet = Wallet.objects.get(id=receiver_id)
                    wallet.balance -= amount
                    receiver_wallet.balance += amount
                    receiver_wallet.save()
        if cancellation_type:
            match transaction_type:
                case TransactionType.DEPOSIT:
                    wallet.balance -= amount
                case TransactionType.WITHDRAW:
                    wallet.balance += amount
                case TransactionType.TRANSFER:
                    receiver_wallet = Wallet.objects.get(id=receiver_id)
                    wallet.balance += amount
                    receiver_wallet.balance -= amount
                    receiver_wallet.save()
            instance.transaction_type = cancellation_type
        wallet.save()
        instance.amount = amount
        instance.save()
        return super().update(instance, validated_data)
