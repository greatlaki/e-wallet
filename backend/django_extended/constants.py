from django.db import models


class TransactionType(models.TextChoices):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"
    TRANSFER = "TRANSFER"
    CANCELLATION = "CANCELLATION"


class RequestMethods(models.TextChoices):
    PATCH = "PATCH"
    DELETE = "DELETE"
