import pytest
from rest_framework.exceptions import ValidationError

from tests.wallets.factories import WalletFactory


@pytest.mark.django_db(transaction=True)
class TestConstraints:
    def test_it_should_raise_exception_if_amount_is_not_positive(self, active_user):
        wallet = WalletFactory.build(
            owner=active_user,
            name="wallet_name",
            wallet_number="test_number",
            amount=-123.12,
        )

        with pytest.raises(ValidationError) as excinfo:
            wallet.save()

        assert excinfo.value.args[0]["amount"] == ["The amount should be positive"]
