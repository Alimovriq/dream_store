from django.contrib import admin

from .models import (
    Products, ProductQuantity, Categories,
    Shop_basket, Shop_basket_items, Orders, OrderItems)


class ShopBasketProductInline(admin.TabularInline):
    model = Shop_basket_items
    extra = 1


class OrderProductInline(admin.TabularInline):
    model = OrderItems
    extra = 1


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    """
    Админка для товаров.
    """

    list_display = (
        'pk',
        'name',
        'price',
        'category',
        'description',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    list_editable = ('price', 'description',)
    ordering = ('-name',)


@admin.register(ProductQuantity)
class ProductQuantityAdmin(admin.ModelAdmin):
    """
    Админка для товаров и их кол-ва.
    """

    list_display = (
        'pk',
        'product',
        'stock',
    )
    list_filter = ('product',)
    list_editable = ('stock',)
    search_fields = ('product',)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """
    Админка для категорий.
    """

    list_display = (
        'pk',
        'name',
        'description',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    list_editable = ('description',)
    ordering = ('-name',)


@admin.register(Shop_basket)
class ShopBasketAdmin(admin.ModelAdmin):
    """
    Админка для корзины.
    """

    list_display = (
        'pk',
        'customer',
    )
    list_filter = ('customer',)
    filter_horizontal = ('products',)
    search_fields = ('customer',)
    inlines = (ShopBasketProductInline,)


@admin.register(Shop_basket_items)
class ShopBasketItemsAdmin(admin.ModelAdmin):
    """
    Админка для объектов корзины.
    """

    list_display = (
        'pk',
        'shop_basket',
        'product',
        'quantity',
    )
    list_filter = ('shop_basket', 'product',)
    list_editable = ('quantity',)
    search_fields = ('shop_basket',)


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    """
    Админка для заказов.
    """

    list_display = (
        'pk',
        'customer',
        'total_price',
        'created_at',
        'address',
        'is_payed',
    )
    list_filter = (
        'customer',
        'is_payed',
        'created_at',
        'total_price',)
    filter_horizontal = ('products',)
    ordering = ('-created_at',)
    search_fields = ('customer', 'address',)
    inlines = (OrderProductInline,)


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    """
    Админка для заказов.
    """

    list_display = (
        'pk',
        'order',
        'product',
        'quantity'
    )
    list_filter = ('order', 'product',)
    list_editable = ('quantity',)
    search_fields = ('order', 'product',)
