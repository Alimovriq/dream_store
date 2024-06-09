# Generated by Django 3.2.3 on 2024-05-11 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0030_alter_orderitemsrefund_order_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitemsrefund',
            name='order_item',
            field=models.ForeignKey(help_text='id товара в Заказе', on_delete=django.db.models.deletion.CASCADE, to='orders.orderitems', verbose_name='Возвращаемый товар'),
        ),
    ]