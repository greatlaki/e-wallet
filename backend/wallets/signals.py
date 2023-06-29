from django.db.models import signals
from django.dispatch import receiver
from django_extended.constants import TransactionType
from wallets.models import Transaction, Wallet


@receiver(signals.pre_delete, sender=Transaction)
def transaction_delete(instance, **kwargs):
    wallet = instance.wallet
    amount = instance.amount
    transaction_type = instance.transaction_type
    receiver_id = instance.receiver.id
    match transaction_type:
        case TransactionType.DEPOSIT:
            wallet.balance -= amount
        case TransactionType.WITHDRAW:
            wallet.balance += amount
        case TransactionType.TRANSFER:
            receiver_wallet = Wallet.objects.get(id=receiver_id)
            wallet.balance += amount
            receiver_wallet.balance -= amount
            receiver_wallet.save()
    wallet.save()
