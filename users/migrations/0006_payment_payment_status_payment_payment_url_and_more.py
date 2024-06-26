# Generated by Django 5.0.3 on 2024-04-03 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(default='unpaid', verbose_name='Статус оплаты'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_url',
            field=models.TextField(blank=True, null=True, verbose_name='Ссылка на оплату'),
        ),
        migrations.AddField(
            model_name='payment',
            name='session_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='id платежной сессии'),
        ),
    ]
