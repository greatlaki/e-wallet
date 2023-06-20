import pytest

from tests.wallets.factories import WalletFactory


@pytest.mark.django_db
class TestPost:
    def test_it_creates_wallet(self, api_client, active_user):
        api_client.force_authenticate(active_user)
        wallet = WalletFactory.build()
        data = {
            "owner": wallet.owner,
            "name": wallet.name,
            "wallet_number": wallet.wallet_number,
            "amount": wallet.amount,
        }

        response = api_client.post("/api/wallets/", data=data, format="json")

        assert response.status_code == 201
