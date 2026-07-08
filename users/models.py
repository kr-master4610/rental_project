from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    TENANT = 'tenant'
    LANDLORD = 'landlord'

    ROLE_CHOICES = [
        (TENANT, 'Арендатор'),
        (LANDLORD, 'Арендодатель'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=TENANT
    )

    # Авторизовываться будем по email, а не по username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"