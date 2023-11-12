# Generated by Django 3.2.3 on 2023-11-12 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_shop_basket_items_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_basket',
            name='products',
            field=models.ManyToManyField(help_text='Выберите товар', related_name='shopbasketproduct', through='products.Shop_basket_items', to='products.Product', verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='shop_basket_items',
            name='product',
            field=models.ForeignKey(help_text='Выберите товар', on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Товар'),
        ),
    ]
