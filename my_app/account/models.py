from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.timesince import timesince
from home.models import Product

from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


class User(AbstractUser):
    GENDER_TYPES = (
        ("women", 'женщина'),
        ("men", 'мужчина'),
    )
    bio = models.TextField('Описание', max_length=500, blank=True)
    date_joined = models.DateTimeField("Дата регистрации", default=timezone.now)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    avatar = models.ImageField("Фото", upload_to='avatars', blank=True, null=True)
    gender = models.CharField("Пол", choices=GENDER_TYPES, max_length=10)
    tel = models.CharField('Телефон', max_length=12)
    auth_code = models.CharField(max_length=6, blank=True)

    def last_login_formatted(self):
        return timesince(self.last_login)

    def __str__(self):
        return f'{self.username}: {self.first_name} - {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Reviews(models.Model):
    """Заказчик"""
    name = models.CharField('Заказчик', max_length=20)
    tel = models.CharField('Телефон', max_length=12)
    product = models.CharField('Название продукта', max_length=250)

    def __str__(self):
        return f"{self.name} - {self.tel} - {self.product}"

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"
