from django.core.management.base import BaseCommand
from faker import Faker
from ...models import User

class Command(BaseCommand):
    help = "create fake user"

    def handle(self, *args, **options):
        fake = Faker(['ka_GE'])
        for _ in range(10):
            email = fake.unique.email()
            name = fake.unique.first_name()
            last_name = fake.unique.last_name()
            tel_number = fake.unique.building_number()
            password = 'password'
            user = User.objects.create(
                email = email,
                first_name=name,
                last_name=last_name,
                tel_number=tel_number,
                password=password
            )
            user.save()