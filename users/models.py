from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Делаем email основным полем для входа вместо username
    email = models.EmailField(unique=True)

    # Поле role полностью удалено, так как у всех одна роль

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email