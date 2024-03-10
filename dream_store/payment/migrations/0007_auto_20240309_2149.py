# Generated by Django 3.2.3 on 2024-03-09 18:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_status'),
        ('payment', '0006_alter_orderpayment_idempotence_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayment',
            name='idempotence_key',
            field=models.UUIDField(default=uuid.UUID('6232f7b7-8a31-4aff-99c4-5c232d8618ba'), editable=False, help_text='Ключ идемпотентности', primary_key=True, serialize=False, verbose_name='Ключ идемпотентности'),
        ),
        migrations.AlterField(
            model_name='orderpayment',
            name='order',
            field=models.ForeignKey(help_text='id Заказа', on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.order', verbose_name='Заказ'),
        ),
    ]