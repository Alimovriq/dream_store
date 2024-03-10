# Generated by Django 3.2.3 on 2024-03-09 12:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPaymenet',
            fields=[
                ('idempotentence_key', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Ключ идемпотентности', primary_key=True, serialize=False, verbose_name='Ключ идемпотентности')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Дата создания', verbose_name='Дата создания')),
                ('order', models.ForeignKey(help_text='id Заказа', on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Оплаченный заказ',
                'verbose_name_plural': 'Оплаченные заказы',
            },
        ),
    ]