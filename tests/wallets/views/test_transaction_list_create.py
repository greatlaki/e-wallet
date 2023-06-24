from decimal import Decimal

import pytest
from django_extended.constants import TransactionType

from tests.users.factories import UserFactory
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

        assert response.status_code == 201
        wallet.refresh_from_db()
        assert data["amount"] == wallet.balance

    def test_it_withdraws_balance_if_user_is_admin(self, api_client, admin_user):
        api_client.force_authenticate(admin_user)
        user = UserFactory()
        wallet = WalletFactory(owner=user, balance=Decimal("100.0"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet.pk,
            "amount": Decimal("100.00"),
            "transaction_type": TransactionType.WITHDRAW,
        }

        response = api_client.post(
            "/api/wallets/transaction/", data=data, format="json"
        )

        assert response.status_code == 201

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

        assert response.status_code == 201
        wallet.refresh_from_db()
        assert wallet.balance == Decimal("1.00")

    def test_it_returns_error_if_amount_is_more_than_balance(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("10.00"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet.pk,
            "amount": Decimal("90.00"),
            "transaction_type": TransactionType.WITHDRAW,
        }

        response = api_client.post(
            "/api/wallets/transaction/", data=data, format="json"
        )

        assert response.status_code == 400
        assert response.data["balance"] == ["The balance should be positive"]

    def test_it_returns_error_if_user_is_not_active(self, api_client, active_user):
        wallet = WalletFactory(owner=active_user)
        TransactionFactory.build()
        data = {
            "wallet_id": wallet.pk,
            "amount": Decimal("99.00"),
            "transaction_type": TransactionType.DEPOSIT,
        }

        response = api_client.post(
            "/api/wallets/transaction/", data=data, format="json"
        )

        assert response.status_code == 401
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )

    def test_it_tops_up_balance_of_another_user(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        user = UserFactory()
        wallet = WalletFactory(owner=user, balance=Decimal("1.0"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet.pk,
            "amount": Decimal("99.00"),
            "transaction_type": TransactionType.DEPOSIT,
        }

        response = api_client.post(
            "/api/wallets/transaction/", data=data, format="json"
        )

        assert response.status_code == 201
        wallet.refresh_from_db()
        assert wallet.balance == Decimal("100.0")

    def test_it_does_not_withdraw_if_user_is_not_owner(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        user = UserFactory()
        wallet = WalletFactory(owner=user, balance=Decimal("100.0"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet.pk,
            "amount": Decimal("100.00"),
            "transaction_type": TransactionType.WITHDRAW,
        }

        response = api_client.post(
            "/api/wallets/transaction/", data=data, format="json"
        )

        assert response.status_code == 400
        assert response.data["wallet"] == ["The user must be the owner of the wallet."]


@pytest.mark.django_db
class TestGet:
    def test_it_returns_transaction(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        TransactionFactory(wallet=wallet, transaction_type=TransactionType.DEPOSIT)

        response = api_client.get("/api/wallets/transaction/")

        assert response.status_code == 200
