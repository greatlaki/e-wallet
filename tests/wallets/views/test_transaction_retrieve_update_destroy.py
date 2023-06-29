# import pytest
# from tests.wallets.factories import WalletFactory, TransactionFactory
#
# from django_extended.constants import TransactionType
#
#
# @pytest.mark.django_db
# class TestPut:
#     def test_it_updates_transaction(self, api_client, active_user):
#         api_client.force_authenticate(active_user)
#         wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
#         transaction = TransactionFactory(
#             wallet=wallet,
#             transaction_type=TransactionType.DEPOSIT,
#             amount=Decimal("10.0"),
#         )
#         data = {
#             "wallet_id": wallet.pk,
#             "transaction_type": TransactionType.DEPOSIT,
#             "amount": Decimal("30.0"),
#         }
#
#         response = api_client.put(
#             f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
#         )
#
#         assert response.status_code == 200
#         wallet.refresh_from_db()
#         assert wallet.balance == Decimal("130.0")
#
#     def test_it_(self, api_client, active_user):
#         # todo: Transaction cancellation, only for admin
#         api_client.force_authenticate(active_user)
#         wallet = WalletFactory(owner=active_user, balance=Decimal("100.00"))
#         transaction = TransactionFactory(
#             wallet=wallet,
#             transaction_type=TransactionType.DEPOSIT,
#             amount=Decimal("10.0"),
#         )
#         data = {
#             "wallet_id": None,
#             "transaction_type": TransactionType.DEPOSIT,
#             "amount": Decimal("30.0"),
#         }
#
#         response = api_client.put(
#             f"/api/wallets/transactions/{transaction.pk}/", data=data, format="json"
#         )
#
#         # assert response.status_code == 200
#         # wallet.refresh_from_db()
#         # assert wallet.balance == Decimal("100.0")
