from decimal import Decimal

from django.db import models

MINIMUM_TRANSFER_RATE = Decimal("0.1")


class UserRole(models.TextChoices):
    ADMIN = "ADMIN"
    WALLET_OWNER = "WALLET_OWNER"


class TransactionType(models.TextChoices):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"
    TRANSFER = "TRANSFER"
    CANCELLATION = "CANCELLATION"


class RequestMethods(models.TextChoices):
    POST = "POST"
    PATCH = "PATCH"
