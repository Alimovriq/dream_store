from django.contrib import admin

from .models import Shop_basket, Shop_basket_items


class ShopBasketProductInline(admin.TabularInline):
    model = Shop_basket_items
    extra = 1


@admin.register(Shop_basket)
class ShopBasketAdmin(admin.ModelAdmin):
    """
    Админка для корзины.
    """

    list_display = (
        'pk',
        'customer',
        'count_products',
        'total_price',
    )
    list_filter = ('customer',)
    filter_horizontal = ('products',)
    search_fields = ('customer',)
    inlines = (ShopBasketProductInline,)

    @admin.display(description='Количество позиций в корзине')
    def count_products(self, obj):
        """
        Отображает кол-во товаров в корзине.
        """

        cartitem = Shop_basket_items.objects.filter(shop_basket=obj)
        quantity = 0
        for _ in cartitem:
            # if item.product:
            quantity += 1
        return quantity

    @admin.display(description='Итоговая стоимость в руб.')
    def total_price(self, obj):
        """
        Отображает итоговую стоимость товаров в корзине.
        """

        cartitem = Shop_basket_items.objects.filter(shop_basket=obj)
        total = 0
        for item in cartitem:
            # if item.product:
            total += item.product.price * item.quantity
        return total


@admin.register(Shop_basket_items)
class ShopBasketItemsAdmin(admin.ModelAdmin):
    """
    Админка товаров для корзин.
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
