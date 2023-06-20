from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint

from django_extended.models import BaseModel
from users.models import User


class Wallet(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField(max_length=255)
    wallet_number = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=32, decimal_places=2, validators=[MinValueValidator(0.0)])

    class Meta:
        constraints = (
            CheckConstraint(
                check=models.Q(amount__gte=0.0),
                name="positive_amount"),
        )
