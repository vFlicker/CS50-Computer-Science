from django.contrib.auth.models import AbstractUser
from django.db import models

# - Категорії
# - Аукціони
# - Ставки
# - Коментарі.
#
# Пам'ятайте, що щоразу, як ви змінюватимете щось в auctions/models.py,
# вам потрібно буде спочатку виконати python manage.py makemigrations,
# а потім python manage.py migrate, щоб перенести ці зміни до вашої бази даних.


class User(AbstractUser):
    pass
