# Generated by Django 3.2.3 on 2024-06-09 12:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0039_alter_orderpayment_idempotence_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayment',
            name='idempotence_key',
            field=models.UUIDField(default=uuid.UUID('60216d8f-103e-45bd-8fdd-075722ade7e6'), editable=False, help_text='Ключ идемпотентности', primary_key=True, serialize=False, verbose_name='Ключ идемпотентности'),
        ),
    ]
