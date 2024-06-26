# Generated by Django 3.2.3 on 2024-03-17 15:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_alter_orderpayment_idempotence_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayment',
            name='idempotence_key',
            field=models.UUIDField(default=uuid.UUID('ba06ddc8-7839-4b04-ad34-99f3dc0e3d02'), editable=False, help_text='Ключ идемпотентности', primary_key=True, serialize=False, verbose_name='Ключ идемпотентности'),
        ),
    ]
