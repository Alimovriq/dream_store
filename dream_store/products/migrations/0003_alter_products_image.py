# Generated by Django 3.2.3 on 2023-10-14 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20231008_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, help_text='Добавить изображние для поста', null=True, upload_to='products/', verbose_name='Изображение'),
        ),
    ]