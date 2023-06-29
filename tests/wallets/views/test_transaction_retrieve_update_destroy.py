from decimal import Decimal

import pytest
from django_extended.constants import TransactionType

from tests.wallets.factories import TransactionFactory, WalletFactory


@pytest.mark.django_db
class TestGet:
    def test_it_returns_transaction(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            receiver=None,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("200.0"),
        )

        response = api_client.get(f"/api/wallets/transactions/{transaction.pk}/")

        assert response.status_code == 200
        assert response.data["id"] == transaction.id

    def test_it_returns_error_if_user_is_not_auth(self, api_client, active_user):
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            receiver=None,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("200.0"),
        )

        response = api_client.get(f"/api/wallets/transactions/{transaction.pk}/")

        assert response.status_code == 401
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )


@pytest.mark.django_db
class TestPatch:
    def test_it_updates_deposit_transaction(self, api_client, admin_user, active_user):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            receiver=None,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("200.0"),
        )
        data = {
            "amount": Decimal("500.0"),
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 200
        wallet.refresh_from_db()
        assert wallet.balance == Decimal("600.0")

    def test_it_allows_admin_user_to_update_transaction(
        self, api_client, admin_user, active_user
    ):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("10.0"),
        )
        data = {
            "amount": Decimal("30.0"),
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 200

    def test_it_does_not_allow_no_admin_user_to_update_transaction(
        self, api_client, active_user, admin_user
    ):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("10.0"),
        )
        data = {
            "amount": Decimal("30.0"),
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "You do not have permission to perform this action."
        )
