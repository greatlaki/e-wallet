from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django_extended.constants import TransactionType

from tests.wallets.factories import TransactionFactory, WalletFactory


@pytest.mark.django_db()
class TestConstraints:
    def test_it_should_raise_error_if_amount_is_less_than_minimum_rate(
        self, active_user
    ):
        wallet = WalletFactory(
            owner=active_user,
            name="wallet_name",
            wallet_number="test_number",
            balance=Decimal("100.0"),
        )

        with pytest.raises(ValidationError):
            TransactionFactory(
                wallet=wallet,
                receiver=None,
                amount=Decimal("0.0"),
                transaction_type=TransactionType.DEPOSIT,
            )