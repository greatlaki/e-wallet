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


@pytest.mark.django_db
class TestGet:
    def test_it_returns_wallets_list_if_user_is_admin(self, api_client, admin_user):
        api_client.force_authenticate(admin_user)
        WalletFactory(owner=admin_user)
        WalletFactory(owner=admin_user)
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

    def test_it_returns_error_if_user_is_not_active(
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
