# Generated by Django 3.2.3 on 2024-03-09 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_status'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpaymenet',
            name='payment_id',
            field=models.CharField(blank=True, help_text='id платежа от Yookassa', max_length=100, null=True, unique=True, verbose_name='id платежа Yookassa'),
        ),
        migrations.AddField(
            model_name='orderpaymenet',
            name='status',
            field=models.CharField(default=1, help_text='Статус платежа', max_length=60, verbose_name='Статус платежа'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderpaymenet',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, editable=False, help_text='Сумма платежа', max_digits=10, verbose_name='Сумма'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderpaymenet',
            name='order',
            field=models.ForeignKey(help_text='id Заказа', on_delete=django.db.models.deletion.CASCADE, related_name='paymenets', to='orders.order', verbose_name='Заказ'),
        ),
    ]