from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Product, Category,
    Brand, CountryProduct)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Админка для брендов.
    """

    list_display = (
        'pk',
        'name',
        'description',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('-name',)


@admin.register(CountryProduct)
class CountryProducyAdmin(admin.ModelAdmin):
    """
    Админка для стран.
    """
    list_display = (
        'pk',
        'name',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админка для товаров.
    """

    list_display = (
        'pk',
        'name',
        'price',
        'quantity',
        'brand',
        'category',
        'description',
        'country',
        'image_preview',
        'meta_title',
        'meta_description',
        'slug',
    )
    list_filter = ('name', 'brand', 'country',)
    search_fields = ('name',)
    list_editable = ('price', 'description', 'quantity')
    ordering = ('-name',)

    @admin.display(description='Изображение')
    def image_preview(self, obj):
        try:
            return format_html(
                '<img src="{}" style="max-width:50px; max-height:50px"/>'.format(
                    obj.image.url))
        except ValueError:
            pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для категорий.
    """

    list_display = (
        'pk',
        'name',
        'description',
        'meta_title',
        'meta_description',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    list_editable = ('description',)
    ordering = ('-name',)
