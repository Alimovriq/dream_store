# Generated by Django 3.2.3 on 2024-03-09 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_rename_idempotentence_key_orderpaymenet_idempotence_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpaymenet',
            name='status',
            field=models.CharField(default='created', help_text='Статус платежа', max_length=60, verbose_name='Статус платежа'),
        ),
    ]