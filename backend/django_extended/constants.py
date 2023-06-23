from django.db import models


class TransactionType(models.TextChoices):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"
