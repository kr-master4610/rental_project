import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking
from faker import Faker
from datetime import date, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Генерация реалистичных тестовых данных с помощью Faker'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начало генерации данных через Faker...")

        # Инициализируем Faker с немецкой локалью, чтобы адреса были аутентичными
        fake = Faker('de_DE')

        landlord = User.objects.filter(role='landlord').first()
        if not landlord:
            self.stdout.write(self.style.ERROR("Сначала создайте пользователя landlord!"))
            return

        housing_types = ["apartment", "house", "room"]

        # Генерируем 10 сочных, случайных объявлений
        for _ in range(10):
            h_type = random.choice(housing_types)
            city = fake.city()

            listing = Listing.objects.create(
                landlord=landlord,
                title=f"Schöne {h_type} in {city}",
                description=fake.paragraph(nb_sentences=4),  # Генерирует реалистичный абзац текста
                location=f"{city}, {fake.street_name()} {fake.building_number()}",  # Реальная немецкая улица и дом
                price=random.randint(500, 2500),  # Случайная цена от 500 до 2500 евро
                rooms=random.randint(1, 5),
                housing_type=h_type,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f"Faker создал объект: {listing.title}"))

            # Каждому третьему объявлению закинем случайную бронь
            if random.choice([True, False, False]):
                start = date(2026, 8, random.randint(1, 10))
                end = start + timedelta(days=random.randint(3, 10))

                Booking.objects.create(
                    listing=listing,
                    tenant=landlord,
                    start_date=start,
                    end_date=end
                )
                self.stdout.write(self.style.WARNING(f"--> Добавлена бронь на даты {start} - {end}"))

        self.stdout.write(self.style.SUCCESS("База успешно заполнена фейковыми данными!"))