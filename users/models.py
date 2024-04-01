from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from materials.models import Course, Lesson
from services import NULLABLE


class UserRoles(models.TextChoices):
    MEMBER = 'member'
    MODERATOR = 'moderator'


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='Номер телефона')
    city = models.CharField(max_length=150, **NULLABLE, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Аватар')

    role = models.CharField(max_length=15, choices=UserRoles.choices, default=UserRoles.MEMBER, verbose_name='Роль')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Пользователь', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='Курс', related_name='paid', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='paid', **NULLABLE)

    payment_date = models.DateTimeField(default=timezone.now, verbose_name='Дата платежа')
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма платежа')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash', verbose_name='Способ платежа')

    def __str__(self):
        return f'{self.course if self.course else self.lesson}, оплачено {self.payment_amount} руб.'

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ('-payment_date',)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'{self.user}, подписка: {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
