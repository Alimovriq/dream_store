from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Product, Category,
    # Shop_basket, Shop_basket_items,
    # Order, OrderItems,
    Brand, CountryProduct)


# class ShopBasketProductInline(admin.TabularInline):
#     model = Shop_basket_items
#     extra = 1


# class OrderProductInline(admin.TabularInline):
#     model = OrderItems
#     extra = 1


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


# @admin.register(Shop_basket)
# class ShopBasketAdmin(admin.ModelAdmin):
#     """
#     Админка для корзины.
#     """

#     list_display = (
#         'pk',
#         'customer',
#         'count_products',
#         'total_price',
#     )
#     list_filter = ('customer',)
#     filter_horizontal = ('products',)
#     search_fields = ('customer',)
#     inlines = (ShopBasketProductInline,)

#     @admin.display(description='Количество позиций в корзине')
#     def count_products(self, obj):
#         """
#         Отображает кол-во товаров в корзине.
#         """

#         cartitem = Shop_basket_items.objects.filter(shop_basket=obj)
#         quantity = 0
#         for item in cartitem:
#             if item.product:
#                 quantity += 1
#         return quantity

#     @admin.display(description='Итоговая стоимость в руб.')
#     def total_price(self, obj):
#         """
#         Отображает итоговую стоимость товаров в корзине.
#         """

#         cartitem = Shop_basket_items.objects.filter(shop_basket=obj)
#         total = 0
#         for item in cartitem:
#             if item.product:
#                 total += item.product.price * item.quantity
#         return total

#     # @admin.display(description='Товары в корзине')
#     # def display_products(self, obj):
#     #     """
#     #     Отображает товары в корзине
#     #     """

#     #     cartitem = Shop_basket_items.objects.filter(shop_basket=obj)
#     #     print(cartitem)
#     #     print("HELLO")
#     #     products_list = []
#     #     for item in cartitem:
#     #         products_list.append(item.product.name)
#     #     return products_list


# @admin.register(Shop_basket_items)
# class ShopBasketItemsAdmin(admin.ModelAdmin):
#     """
#     Админка для объектов корзины.
#     """

#     list_display = (
#         'pk',
#         'shop_basket',
#         'product',
#         'quantity',
#     )
#     list_filter = ('shop_basket', 'product',)
#     list_editable = ('quantity',)
#     search_fields = ('shop_basket',)


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     """
#     Админка для заказов.
#     """

#     list_display = (
#         'pk',
#         'customer',
#         'total_price',
#         'created_at',
#         'address',
#         'is_payed',
#     )
#     list_filter = (
#         'customer',
#         'is_payed',
#         'created_at',
#         'total_price',)
#     filter_horizontal = ('products',)
#     ordering = ('-created_at',)
#     search_fields = ('customer', 'address',)
#     inlines = (OrderProductInline,)


# @admin.register(OrderItems)
# class OrderItemsAdmin(admin.ModelAdmin):
#     """
#     Админка для заказов.
#     """

#     list_display = (
#         'pk',
#         'order',
#         'product',
#         'quantity'
#     )
#     list_filter = ('order', 'product',)
#     list_editable = ('quantity',)
#     search_fields = ('order', 'product',)
