from decimal import Decimal

import pytest
from django_extended.constants import TransactionType
from wallets.models import Transaction

from tests.users.factories import UserFactory
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

    def test_it_updated_withdraw_transaction(self, api_client, admin_user, active_user):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("90.0"),
        )
        data = {
            "amount": Decimal("9.0"),
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 200
        wallet.refresh_from_db()
        assert wallet.balance == Decimal("91.0")

    def test_it_updated_transfer_transaction(self, api_client, admin_user, active_user):
        api_client.force_authenticate(admin_user)
        user = UserFactory()
        wallet1 = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        wallet2 = WalletFactory(owner=user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet1,
            receiver=wallet2,
            transaction_type=TransactionType.TRANSFER,
            amount=Decimal("100.0"),
        )

        data = {
            "amount": Decimal("10.0"),
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 200
        wallet1.refresh_from_db()
        wallet2.refresh_from_db()
        assert wallet1.balance == Decimal("90.0")
        assert wallet2.balance == Decimal("110.0")

    def test_it_allows_admin_user_to_cancel_deposit_transaction(
        self, api_client, admin_user, active_user
    ):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("100.0"),
        )
        data = {
            "transaction_type": TransactionType.CANCELLATION,
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 200
        wallet.refresh_from_db()
        transaction.refresh_from_db()
        assert wallet.balance == Decimal("100")
        assert transaction.transaction_type == TransactionType.CANCELLATION

    def test_it_allows_admin_user_to_cancel_withdraw_transaction(
        self, api_client, admin_user, active_user
    ):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("100.0"),
        )
        data = {
            "transaction_type": TransactionType.CANCELLATION,
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 200
        wallet.refresh_from_db()
        transaction.refresh_from_db()
        assert wallet.balance == Decimal("100")
        assert transaction.transaction_type == TransactionType.CANCELLATION

    def test_it_allows_admin_user_to_cancel_transfer_transaction(
        self, api_client, admin_user, active_user
    ):
        api_client.force_authenticate(admin_user)
        user = UserFactory()
        wallet1 = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        wallet2 = WalletFactory(owner=user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet1,
            receiver=wallet2,
            transaction_type=TransactionType.TRANSFER,
            amount=Decimal("100.0"),
        )

        data = {
            "transaction_type": TransactionType.CANCELLATION,
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 200
        wallet1.refresh_from_db()
        wallet2.refresh_from_db()
        assert wallet1.balance == Decimal("100")
        assert wallet2.balance == Decimal("100")
        transaction.refresh_from_db()
        assert transaction.transaction_type == TransactionType.CANCELLATION

    def test_it_returns_error_if_user_want_to_cancel_transaction(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("100.0"),
        )
        data = {
            "transaction_type": TransactionType.CANCELLATION,
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "You do not have permission to perform this action."
        )

    def test_it_does_not_allow_no_admin_user_to_update_transaction(
        self, api_client, active_user
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

    def test_it_returns_error_if_amount_is_zero(
        self, api_client, active_user, admin_user
    ):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("10.0"),
        )
        data = {
            "amount": Decimal("0.0"),
        }

        response = api_client.patch(
            f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
        )

        assert response.status_code == 400
        assert (
            response.data["amount"]["amount"]
            == "Insufficient transfer amount, the minimum amount is 0.1"
        )


@pytest.mark.django_db
class TestDelete:
    def test_it_deletes_transaction(self, api_client, admin_user, active_user):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("1000.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("500.0"),
        )
        assert Transaction.objects.count() == 1

        response = api_client.delete(f"/api/wallets/transactions/{transaction.pk}/")

        assert response.status_code == 204
        assert Transaction.objects.count() == 0

    def test_it_returns_error_if_user_deletes_transaction(
        self, api_client, active_user
    ):
        user = UserFactory()
        api_client.force_authenticate(user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        transaction = TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("500.0"),
        )

        response = api_client.delete(f"/api/wallets/transactions/{transaction.pk}/")

        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "You do not have permission to perform this action."
        )
