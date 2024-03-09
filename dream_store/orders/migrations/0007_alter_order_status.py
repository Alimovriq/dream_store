# Generated by Django 3.2.3 on 2024-03-09 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Активный'), ('ENDED', 'Завершенный'), ('CANCELLED', 'Отмененный')], default='ACTIVE', max_length=300, verbose_name='Статус Заказа'),
        ),
    ]
