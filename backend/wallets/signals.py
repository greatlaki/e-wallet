from django.db.models import signals
from django.dispatch import receiver
from wallets.models import Transaction
from wallets.services import cancel_wallet_transactions


@receiver(signals.pre_delete, sender=Transaction)
def transaction_delete(instance, **kwargs):
    wallet_id = instance.wallet.pk
    amount = instance.amount
    transaction_type = instance.transaction_type
    receiver_id = instance.receiver.id
    cancel_wallet_transactions(wallet_id, receiver_id, amount, transaction_type)
