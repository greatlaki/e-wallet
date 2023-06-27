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
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 201
        wallet.refresh_from_db()
        assert data["amount"] == wallet.balance

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
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 201
        wallet.refresh_from_db()
        assert wallet.balance == Decimal("100.0")

    def test_it_withdraws_amount_from_another_user_if_auth_user_is_admin(
        self, api_client, admin_user
    ):
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
            "/api/wallets/transactions/", data=data, format="json"
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
            "/api/wallets/transactions/", data=data, format="json"
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
            "/api/wallets/transactions/", data=data, format="json"
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
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 401
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )

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
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 400
        assert response.data["wallet_id"] == [
            "The user must be the owner of the wallet."
        ]

    def test_it_sends_amount(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        user = UserFactory()
        wallet1 = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        wallet2 = WalletFactory(owner=user, balance=Decimal("100.00"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet1.pk,
            "receiver_id": wallet2.pk,
            "amount": Decimal("50.00"),
            "transaction_type": TransactionType.TRANSFER,
        }

        response = api_client.post(
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 201
        wallet1.refresh_from_db()
        wallet2.refresh_from_db()
        assert wallet1.balance == Decimal("50")
        assert wallet2.balance == Decimal("150")

    def test_it_returns_error_if_sender_balance_is_less_than_amount(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        user = UserFactory()
        wallet1 = WalletFactory(owner=active_user, balance=Decimal("1.00"))
        wallet2 = WalletFactory(owner=user, balance=Decimal("100.00"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet1.pk,
            "receiver_id": wallet2.pk,
            "amount": Decimal("50.00"),
            "transaction_type": TransactionType.TRANSFER,
        }

        response = api_client.post(
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 400
        assert response.data["balance"] == ["The balance should be positive"]

    def test_it_returns_error_if_wallets_do_not_exist(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        TransactionFactory.build()
        data = {
            "wallet_id": 123,
            "receiver_id": 321,
            "amount": Decimal("5.00"),
            "transaction_type": TransactionType.TRANSFER,
        }

        response = api_client.post(
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 400
        assert response.data["wallet_id"]["wallet_id"] == "The wallet does not exist."
        assert (
            response.data["receiver_id"]["receiver_id"] == "The wallet does not exist."
        )

    def test_it_returns_error_if_receiver_wallet_was_not_entered(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet.pk,
            "amount": Decimal("5.00"),
            "transaction_type": TransactionType.TRANSFER,
        }

        response = api_client.post(
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 400
        assert response.data["receiver_id"] == [
            "The wallet of the recipient must be entered."
        ]

    def test_it_returns_error_if_user_is_not_owner_of_sender_wallet(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        user1 = UserFactory()
        user2 = UserFactory()
        wallet1 = WalletFactory(owner=user1, balance=Decimal("100.00"))
        wallet2 = WalletFactory(owner=user2, balance=Decimal("10.00"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet1.pk,
            "receiver_id": wallet2.pk,
            "amount": Decimal("5.00"),
            "transaction_type": TransactionType.TRANSFER,
        }

        response = api_client.post(
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 400
        assert response.data["wallet_id"] == [
            "The user must be the owner of the wallet."
        ]

    def test_it_sends_amount_if_auth_user_is_admin(
        self, api_client, active_user, admin_user
    ):
        api_client.force_authenticate(admin_user)
        user = UserFactory()
        wallet1 = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        wallet2 = WalletFactory(owner=user, balance=Decimal("10.00"))
        TransactionFactory.build()
        data = {
            "wallet_id": wallet1.pk,
            "receiver_id": wallet2.pk,
            "amount": Decimal("50.00"),
            "transaction_type": TransactionType.TRANSFER,
        }

        response = api_client.post(
            "/api/wallets/transactions/", data=data, format="json"
        )

        assert response.status_code == 201
        wallet1.refresh_from_db()
        wallet2.refresh_from_db()
        assert wallet1.balance == Decimal("50")
        assert wallet2.balance == Decimal("60")


@pytest.mark.django_db
class TestGet:
    def test_it_returns_transaction(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        user = UserFactory()
        wallet1 = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        wallet2 = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        wallet3 = WalletFactory(owner=user, balance=Decimal("0.00"))
        TransactionFactory(
            wallet=wallet1,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("2.0"),
        )
        TransactionFactory(
            wallet=wallet1,
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("2.0"),
        )
        TransactionFactory(
            wallet=wallet2,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("2.0"),
        )
        TransactionFactory(
            wallet=wallet2,
            receiver=wallet3,
            transaction_type=TransactionType.TRANSFER,
            amount=Decimal("100.0"),
        )
        response = api_client.get("/api/wallets/transactions/")

        assert response.status_code == 200
        assert len(response.data) == 4

    def test_it_users_transactions_if_auth_user_is_admin(
        self, api_client, active_user, admin_user
    ):
        api_client.force_authenticate(admin_user)
        user = UserFactory()
        wallet1 = WalletFactory(owner=user, balance=Decimal("100.00"))
        wallet2 = WalletFactory(owner=active_user, balance=Decimal("100.00"))

        TransactionFactory(
            wallet=wallet1,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("20.0"),
        )
        TransactionFactory(
            wallet=wallet1,
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("2.0"),
        )
        TransactionFactory(
            wallet=wallet2,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("2.0"),
        )
        TransactionFactory(
            wallet=wallet2,
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("20.0"),
        )

        response = api_client.get("/api/wallets/transactions/")

        assert response.status_code == 200
        assert len(response.data) == 4

    def test_it_returns_error_if_user_is_not_active(self, api_client, active_user):
        wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        TransactionFactory(
            wallet=wallet,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("2.0"),
        )

        response = api_client.get("/api/wallets/transactions/")

        assert response.status_code == 401
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )

    def test_it(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        user1 = UserFactory()
        user2 = UserFactory()
        wallet1 = WalletFactory(owner=active_user, balance=Decimal("100.00"))
        wallet2 = WalletFactory(owner=user1, balance=Decimal("100.00"))
        wallet3 = WalletFactory(owner=user2, balance=Decimal("0.00"))
        TransactionFactory(
            wallet=wallet2,
            receiver=wallet1,
            transaction_type=TransactionType.TRANSFER,
            amount=Decimal("40.0"),
        )
        TransactionFactory(
            wallet=wallet3,
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("40.0"),
        )
        TransactionFactory(
            wallet=wallet3,
            receiver=wallet2,
            transaction_type=TransactionType.TRANSFER,
            amount=Decimal("40.0"),
        )
        response = api_client.get("/api/wallets/transactions/")

        assert response.status_code == 200
