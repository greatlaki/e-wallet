from django.core.validators import MinValueValidator
from django.db import IntegrityError, models
from django.db.models import CheckConstraint
from django_extended.models import BaseModel
from rest_framework.exceptions import ValidationError
from users.models import User


class Wallet(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField(max_length=255)
    wallet_number = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(
        max_digits=32, decimal_places=2, validators=[MinValueValidator(0.0)]
    )

    def save(self, *args, **kwargs):
        try:
            return super().save(*args, **kwargs)
        except IntegrityError as exc:
            if "positive_amount" in str(exc.args):
                error_message = {"amount": ["The amount should be positive"]}
            else:
                raise exc
            raise ValidationError(error_message)

    class Meta:
        constraints = (
            CheckConstraint(check=models.Q(amount__gte=0.0), name="positive_amount"),
        )
