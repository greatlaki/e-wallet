import factory
from wallets.models import Wallet

from tests.users.factories import UserFactory


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    owner = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(
        lambda n: f"wallet of {n.owner.first_name} {n.owner.last_name}"
    )
    wallet_number = factory.Faker("random_number")
    balance = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
