# Generated by Django 3.2.3 on 2024-03-17 15:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0017_alter_orderpayment_idempotence_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayment',
            name='idempotence_key',
            field=models.UUIDField(default=uuid.UUID('3614046d-1bd4-4a2c-8ebd-ccd76c2cc337'), editable=False, help_text='Ключ идемпотентности', primary_key=True, serialize=False, verbose_name='Ключ идемпотентности'),
        ),
    ]