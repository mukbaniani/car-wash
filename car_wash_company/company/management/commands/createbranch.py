from django.core.management.base import BaseCommand
from faker import Faker
from ...models import Branch

class Command(BaseCommand):
    help = "create fake branch"

    def handle(self, *args, **options):
        fake = Faker(['ka_GE'])
        for _ in range(10):
            address = fake.unique.address()
            work_days = "ორშაბათი პარასკევი 9-18"
            tel_number = fake.unique.building_number()
            user = Branch.objects.create(
                address = address,
                work_days=work_days,
                tel_number=tel_number,
                garage_amount=10
            )
            user.save()