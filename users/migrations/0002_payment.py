# Generated by Django 5.0.3 on 2024-03-27 14:03

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(default=datetime.datetime(2024, 3, 27, 14, 3, 20, 422123, tzinfo=datetime.timezone.utc), verbose_name='Дата платежа')),
                ('payment_amount', models.PositiveIntegerField(verbose_name='Сумма платежа')),
                ('payment_method', models.CharField(choices=[('cash', 'Наличные'), ('transfer', 'Перевод')], default='cash', max_length=20, verbose_name='Способ платежа')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='paid', to='materials.course', verbose_name='Курс')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paid', to='materials.lesson', verbose_name='Пользователь')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Платёж',
                'verbose_name_plural': 'Платежи',
                'ordering': ('-payment_date',),
            },
        ),
    ]
