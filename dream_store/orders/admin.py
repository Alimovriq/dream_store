from django.contrib import admin

from .models import Order, OrderItems, OrderRefund, OrderItemsRefund


class OrderProductInline(admin.TabularInline):
    model = OrderItems
    extra = 0


class OrderRefundProductInLine(admin.TabularInline):
    model = OrderItemsRefund
    verbose_name = 'Возвращаемый товар'
    verbose_name_plural = 'Возвращаемые товары'
    fields = ('order_item', 'quantity',)
    extra = 0


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
        'phone',
        'email',
        'address',
        'show_comment',
        'status',
        'is_payed',
    )
    list_filter = (
        'customer',
        'is_payed',
        'status',
        'created_at',
        'total_price',)
    filter_horizontal = ('products',)
    ordering = ('-created_at',)
    search_fields = ('customer', 'address',)
    inlines = (OrderProductInline,)

    @admin.display(description='Комментарий')
    def show_comment(self, obj):
        comment = obj.comment
        return (
            comment[:50] + '...' if len(comment) > 50 else comment)


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


@admin.register(OrderRefund)
class OrderRefundAdmin(admin.ModelAdmin):
    """
    Админка для модели возврата.
    """

    list_display = (
        'pk',
        'order',
        'created_at',
        'comment',
    )
    list_filter = ('order',)
    search_fields = ('order',)
    inlines = (OrderRefundProductInLine,)


@admin.register(OrderItemsRefund)
class OrderRefundItemsAdmin(admin.ModelAdmin):
    """
    Админка для возвращаемых товаров.
    """

    list_display = (
        'pk',
        'order_item',
        'refund',
        'quantity',
    )
    list_filter = ('order_item', 'refund',)
    search_filter = ('order_item', 'refund',)
