import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing
from bookings.models import Booking
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    help = 'Генерация реалистичных тестовых данных с помощью Faker'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начало генерации данных через Faker...")

        # Инициализируем Faker с немецкой локалью
        fake = Faker('de_DE')

        # Автоматически создаем тестовых пользователей, если база пуста
        landlord, created_l = User.objects.get_or_create(
            username="landlord_jack",
            defaults={"email": "jack@example.com", "first_name": "Jack"}
        )
        if created_l:
            landlord.set_password("password123")
            landlord.save()
            self.stdout.write(self.style.SUCCESS("Создан тестовый пользователь-хозяин: landlord_jack"))

        tenant, created_t = User.objects.get_or_create(
            username="tenant_marta",
            defaults={"email": "marta@example.com", "first_name": "Marta"}
        )
        if created_t:
            tenant.set_password("password123")
            tenant.save()
            self.stdout.write(self.style.SUCCESS("Создан тестовый пользователь-арендатор: tenant_marta"))

        housing_types = ["apartment", "house", "room"]

        # Генерируем 10 сочных, случайных объявлений
        for _ in range(10):
            h_type = random.choice(housing_types)
            city = fake.city()

            listing = Listing.objects.create(
                landlord=landlord,
                title=f"Schöne {h_type} in {city}",
                description=fake.paragraph(nb_sentences=4),
                location=f"{city}, {fake.street_name()} {fake.building_number()}",
                price=random.randint(500, 2500),
                rooms=random.randint(1, 5),
                housing_type=h_type,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f"Faker создал объект: {listing.title}"))

            # Каждому третьему объявлению закинем случайную бронь от лица Marta
            if random.choice([True, False, False]):
                start = date(2026, 8, random.randint(1, 10))
                end = start + timedelta(days=random.randint(3, 10))

                Booking.objects.create(
                    listing=listing,
                    tenant=tenant,
                    start_date=start,
                    end_date=end
                )
                self.stdout.write(self.style.WARNING(f"--> Добавлена бронь на даты {start} - {end}"))

        self.stdout.write(self.style.SUCCESS("База успешно заполнена фейковыми данными!"))