# Generated by Django 3.2.3 on 2024-03-09 19:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_auto_20240309_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayment',
            name='idempotence_key',
            field=models.UUIDField(default=uuid.UUID('b15ae908-af55-473f-ab28-dea55cca1c45'), editable=False, help_text='Ключ идемпотентности', primary_key=True, serialize=False, verbose_name='Ключ идемпотентности'),
        ),
        migrations.AlterField(
            model_name='orderpayment',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, help_text='Сумма платежа', max_digits=12, verbose_name='Сумма'),
        ),
    ]
