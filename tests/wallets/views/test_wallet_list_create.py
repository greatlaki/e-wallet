from decimal import Decimal

import pytest

from tests.wallets.factories import WalletFactory


@pytest.mark.django_db
class TestPost:
    def test_it_creates_wallet_by_active_user(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory.build()
        data = {
            "name": wallet.name,
            "wallet_number": wallet.wallet_number,
            "amount": wallet.amount,
        }

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 201
        assert response.data["owner"] == active_user.pk

    def test_it_creates_wallet_by_admin_user(self, api_client, admin_user):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory.build()
        data = {
            "name": wallet.name,
            "wallet_number": wallet.wallet_number,
            "amount": wallet.amount,
        }

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 201
        assert response.data["owner"] == admin_user.pk

    def test_it_returns_error_if_user_is_not_active(self, api_client):
        wallet = WalletFactory.build()
        data = {
            "name": wallet.name,
            "wallet_number": wallet.wallet_number,
            "amount": wallet.amount,
        }

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 401
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )

    def test_it_returns_error_if_amount_is_not_positive(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory.build()
        data = {
            "name": wallet.name,
            "wallet_number": wallet.wallet_number,
            "amount": Decimal("-10"),
        }

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 400
        assert response.data["amount"] == [
            "Ensure this value is greater than or equal to 0.0."
        ]

    def test_it_returns_error_if_amount_has_more_than_2_decimal_places(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory.build()
        data = {
            "name": wallet.name,
            "wallet_number": wallet.wallet_number,
            "amount": Decimal("10.1234"),
        }

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 400
        assert response.data["amount"] == [
            "Ensure that there are no more than 2 decimal places."
        ]

    def test_it_returns_error_if_amount_has_more_than_32_digits_in_total(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory.build()
        data = {
            "name": wallet.name,
            "wallet_number": wallet.wallet_number,
            "amount": Decimal("123412341234123412341234123412341234.00"),
        }

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 400
        assert response.data["amount"] == [
            "Ensure that there are no more than 32 digits in total."
        ]

    def test_it_returns_error_if_required_fields_were_not_entered(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        WalletFactory.build()
        data = {}

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 400
        assert response.data["name"][0] == "This field is required."
        assert response.data["wallet_number"][0] == "This field is required."
        assert response.data["amount"][0] == "This field is required."

    def test_it_returns_error_if_wallet_number_already_exists(
        self, api_client, active_user
    ):
        WalletFactory(wallet_number="test_number")

        api_client.force_authenticate(active_user)
        wallet = WalletFactory.build()
        data = {
            "name": wallet.name,
            "wallet_number": "test_number",
            "amount": wallet.amount,
        }

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 400
        assert response.data["wallet_number"] == ["The wallet number already exists"]

    def test_it_returns_error_if_wallet_number_already_exists_in_another_case(
        self, api_client, active_user
    ):
        WalletFactory(wallet_number="Test_Number")

        api_client.force_authenticate(active_user)
        wallet = WalletFactory.build()
        data = {
            "name": wallet.name,
            "wallet_number": "test_number",
            "amount": wallet.amount,
        }

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 400
        assert response.data["wallet_number"] == ["The wallet number already exists"]


@pytest.mark.django_db
class TestGet:
    def test_it_returns_wallets_list_if_user_is_admin(
        self, api_client, active_user, admin_user
    ):
        api_client.force_authenticate(admin_user)
        WalletFactory(owner=active_user)
        WalletFactory(owner=active_user)
        WalletFactory(owner=admin_user)
        WalletFactory(owner=admin_user)

        response = api_client.get("/api/wallets/")

        assert response.status_code == 200
        assert len(response.data) == 4

    def test_it_returns_empty_wallets_list_if_user_is_not_owner(
        self, api_client, admin_user, active_user
    ):
        api_client.force_authenticate(active_user)
        WalletFactory(owner=admin_user)
        WalletFactory(owner=admin_user)

        response = api_client.get("/api/wallets/")

        assert response.status_code == 200
        assert len(response.data) == 0

    def test_it_returns_wallets_list_of_owner(
        self, api_client, admin_user, active_user
    ):
        api_client.force_authenticate(active_user)
        WalletFactory(owner=active_user)
        WalletFactory(owner=active_user)
        WalletFactory(owner=active_user)
        WalletFactory(owner=admin_user)
        WalletFactory(owner=admin_user)

        response = api_client.get("/api/wallets/")

        assert response.status_code == 200
        assert len(response.data) == 3

    def test_it_returns_error_if_user_is_not_auth(
        self, api_client, active_user, admin_user
    ):
        WalletFactory(owner=active_user)
        WalletFactory(owner=active_user)
        WalletFactory(owner=active_user)
        WalletFactory(owner=admin_user)
        WalletFactory(owner=admin_user)

        response = api_client.get("/api/wallets/")

        assert response.status_code == 401
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )
