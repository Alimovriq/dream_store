# Generated by Django 3.2.3 on 2024-03-17 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_alter_orderitemsrefund_order_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitemsrefund',
            name='order_item',
            field=models.ForeignKey(help_text='id товара в Заказе', limit_choices_to={'order': models.ForeignKey(help_text='id возвращаемого Заказа', on_delete=django.db.models.deletion.CASCADE, related_name='orderitemsrefunds', to='orders.orderrefund', verbose_name='Возврат')}, on_delete=django.db.models.deletion.CASCADE, related_name='refunds', to='orders.orderitems', verbose_name='Возвращаемый товар'),
        ),
    ]