from decimal import Decimal

import pytest

from tests.wallets.factories import WalletFactory


@pytest.mark.django_db
class TestGet:
    def test_it_returns_active_user_balance(
        self,
        api_client,
        active_user,
    ):
        api_client.force_authenticate(active_user)
        WalletFactory(owner=active_user, balance=Decimal("13.00"))
        WalletFactory(owner=active_user, balance=Decimal("13.00"))
        wallet = WalletFactory(owner=active_user, balance=Decimal("123.00"))

        response = api_client.get(f"/api/wallets/{wallet.pk}/balance/")

        assert response.status_code == 200
        assert response.data["balance"] == "123.00"

    def test_it_returns_error_if_user_is_not_auth(
        self,
        api_client,
        active_user,
    ):
        wallet = WalletFactory(owner=active_user, balance=Decimal("123.00"))

        response = api_client.get(f"/api/wallets/{wallet.pk}/balance/")

        assert response.status_code == 401
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )

    def test_it_returns_user_balance_if_auth_user_is_admin(
        self, api_client, active_user, admin_user
    ):
        api_client.force_authenticate(admin_user)
        WalletFactory(owner=active_user, balance=Decimal("32.00"))
        WalletFactory(owner=active_user, balance=Decimal("44.00"))
        wallet = WalletFactory(owner=active_user, balance=Decimal("1.00"))

        response = api_client.get(f"/api/wallets/{wallet.pk}/balance/")

        assert response.status_code == 200
        assert response.data["balance"] == "1.00"
