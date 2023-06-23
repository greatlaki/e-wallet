from decimal import Decimal

import pytest
from django_extended.constants import TransactionType

from tests.wallets.factories import TransactionFactory, WalletFactory


@pytest.mark.django_db
class TestPost:
    def test_it_tops_up_balance(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("0"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet.pk,
            "amount": Decimal("100.00"),
            "transaction_type": TransactionType.DEPOSIT,
        }

        response = api_client.post(
            "/api/wallets/transaction/", data=data, format="json"
        )

        wallet.refresh_from_db()
        assert response.status_code == 201
        assert data["amount"] == wallet.balance

    def test_it_withdraws_from_wallet_balance(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet.pk,
            "amount": Decimal("99.00"),
            "transaction_type": TransactionType.WITHDRAW,
        }

        response = api_client.post(
            "/api/wallets/transaction/", data=data, format="json"
        )

        wallet.refresh_from_db()
        assert response.status_code == 201
        assert wallet.balance == Decimal("1.00")


@pytest.mark.django_db
class TestGet:
    def test_it(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        TransactionFactory(wallet=wallet, transaction_type=TransactionType.DEPOSIT)

        response = api_client.get("/api/wallets/transaction/")

        assert response.status_code == 200
