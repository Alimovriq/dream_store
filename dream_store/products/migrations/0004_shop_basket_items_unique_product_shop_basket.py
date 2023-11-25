# Generated by Django 3.2.3 on 2023-11-08 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_brand_slug'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='shop_basket_items',
            constraint=models.UniqueConstraint(fields=('product', 'shop_basket'), name='unique_product_shop_basket'),
        ),
    ]