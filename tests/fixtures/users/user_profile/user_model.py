from pytest_factoryboy import register
from faker import Factory as FakerFactory
import factory
from app.users.user_profile.models import UserProfile

faker = FakerFactory.create()


@register(_name='user_profile')
class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyAttribute(lambda a: f'{a.username}@example.com'.lower().replace(' ', '_'))
    name = factory.LazyAttribute(lambda a: a.username)


if __name__ == "__main__":
    print(UserProfileFactory())
