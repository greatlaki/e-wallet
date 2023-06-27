from django.core.validators import MinValueValidator
from django.db import IntegrityError, models
from django.db.models import CheckConstraint
from django_extended.constants import TransactionType
from django_extended.models import BaseModel
from rest_framework.exceptions import ValidationError
from users.models import User


class Wallet(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField(max_length=255)
    wallet_number = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(
        max_digits=32, decimal_places=2, validators=[MinValueValidator(0.0)]
    )

    def save(self, *args, **kwargs):
        try:
            return super().save(*args, **kwargs)
        except IntegrityError as exc:
            if "positive_balance" in str(exc.args):
                error_message = {"balance": ["The balance should be positive"]}
            else:
                raise exc
            raise ValidationError(error_message)

    class Meta:
        constraints = (
            CheckConstraint(check=models.Q(balance__gte=0.0), name="positive_balance"),
        )


class Transaction(BaseModel):
    wallet = models.ForeignKey(
        "Wallet",
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    receiver = models.ForeignKey(
        "Wallet",
        on_delete=models.CASCADE,
        related_name="incoming_transactions",
    )
    amount = models.DecimalField(
        max_digits=32, decimal_places=2, validators=[MinValueValidator(0.0)]
    )
    transaction_type = models.CharField(choices=TransactionType.choices)
