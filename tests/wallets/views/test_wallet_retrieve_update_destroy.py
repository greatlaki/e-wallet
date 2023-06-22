from decimal import Decimal

import pytest

from tests.wallets.factories import WalletFactory


@pytest.mark.django_db
class TestGet:
    def test_it_returns_wallet(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )

        response = api_client.get(f"/api/wallets/{wallet.pk}/")

        assert response.status_code == 200

    def test_it_returns_error_if_user_is_not_auth(self, api_client, active_user):
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )

        response = api_client.get(f"/api/wallets/{wallet.pk}/")

        assert response.status_code == 401
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )

    def test_it_returns_wallet_if_user_is_admin(
        self, api_client, active_user, admin_user
    ):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )

        response = api_client.get(f"/api/wallets/{wallet.pk}/")

        assert response.status_code == 200


@pytest.mark.django_db
class TestPut:
    def test_it_updates_wallet(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )
        data = {
            "name": "new_name",
            "wallet_number": "new_wallet_number",
            "amount": Decimal("123.00"),
        }

        response = api_client.put(
            f"/api/wallets/{wallet.pk}/", data=data, format="json"
        )

        wallet.refresh_from_db()
        assert response.status_code == 200
        assert data["name"] == wallet.name
        assert data["wallet_number"] == wallet.wallet_number
        assert data["amount"] == wallet.amount

    def test_it_returns_error_if_wallet_number_already_exists(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )
        WalletFactory(
            owner=active_user, name="name", wallet_number="r2d2", amount=Decimal("0.0")
        )
        data = {
            "name": "new_name",
            "wallet_number": "r2d2",
            "amount": Decimal("144.00"),
        }

        response = api_client.put(
            f"/api/wallets/{wallet.pk}/", data=data, format="json"
        )

        wallet.refresh_from_db()
        assert response.status_code == 400
        assert response.data["wallet_number"] == ["The wallet number already exists"]

    def test_it_returns_error_if_wallet_number_already_exists_in_another_case(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )
        WalletFactory(
            owner=active_user, name="name", wallet_number="r2d2", amount=Decimal("0.0")
        )
        data = {
            "name": "new_name",
            "wallet_number": "R2D2",
            "amount": Decimal("144.00"),
        }

        response = api_client.put(
            f"/api/wallets/{wallet.pk}/", data=data, format="json"
        )

        wallet.refresh_from_db()
        assert response.status_code == 400
        assert response.data["wallet_number"] == ["The wallet number already exists"]

    def test_it_returns_error_if_required_fields_were_not_entered(
        self, api_client, active_user
    ):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )
        data = {
            "amount": Decimal("144.00"),
        }

        response = api_client.put(
            f"/api/wallets/{wallet.pk}/", data=data, format="json"
        )

        wallet.refresh_from_db()
        assert response.status_code == 400
        assert response.data["name"][0] == "This field is required."
        assert response.data["wallet_number"][0] == "This field is required."


@pytest.mark.django_db
class TestPatch:
    def test_it_updates_wallet_partly(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )
        data = {
            "name": "new_name",
            "amount": Decimal("144.00"),
        }

        response = api_client.patch(
            f"/api/wallets/{wallet.pk}/", data=data, format="json"
        )

        wallet.refresh_from_db()
        assert response.status_code == 200
        assert data["name"] == wallet.name
        assert data["amount"] == wallet.amount


@pytest.mark.django_db
class TestDelete:
    def test_it_deletes_wallet(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )

        response = api_client.delete(f"/api/wallets/{wallet.pk}/")

        assert response.status_code == 204

    def test_it_deletes_wallet_by_admin(self, api_client, active_user, admin_user):
        api_client.force_authenticate(admin_user)
        wallet = WalletFactory(
            owner=active_user,
            name="name",
            wallet_number="wallet_number",
            amount=Decimal("0.0"),
        )

        response = api_client.delete(f"/api/wallets/{wallet.pk}/")

        assert response.status_code == 204
