from django.core.management.base import BaseCommand

from faker import Faker

from hotel.models import Hotel, Guest, Stay


class Command(BaseCommand):
    help = "Easy way to initialize the database with some data"

    def handle(self, *args, **kwargs):
        Hotel.objects.all().delete()
        Stay.objects.all().delete()
        Guest.objects.all().delete()

        hotel = Hotel.objects.create(name="Hotel", city="Berlin")
        for i in range(100):
            fake = Faker()
            guest, _ = Guest.objects.get_or_create(phone=fake.phone_number(), defaults={"name": fake.name()})
            if _:
                Stay.objects.create(
                    hotel=hotel,
                    guest=guest,
                )

        print("Done")

