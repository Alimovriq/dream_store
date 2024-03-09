# Generated by Django 3.2.3 on 2024-03-09 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('AC', 'Активный'), ('EN', 'Завершенный'), ('CA', 'Отмененный')], max_length=300, verbose_name='Статус Заказа'),
        ),
    ]
