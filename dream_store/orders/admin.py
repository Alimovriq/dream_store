from django.contrib import admin

from .models import Order, OrderItems


class OrderProductInline(admin.TabularInline):
    model = OrderItems
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
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
