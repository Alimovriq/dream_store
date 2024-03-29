# Generated by Django 3.2.3 on 2024-03-09 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Активный'), ('ENDED', 'Завершенный'), ('CANCELED', 'Отмененный')], default='ACTIVE', max_length=300, verbose_name='Статус Заказа'),
        ),
    ]
