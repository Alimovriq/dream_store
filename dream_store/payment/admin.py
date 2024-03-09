from django.contrib import admin

from .models import OrderPaymenet


@admin.register(OrderPaymenet)
class OrderPaymentAdmin(admin.ModelAdmin):
    """
    Админка для оплаченных Заказов.
    """

    list_display = (
        'idempotentence_key',
        'order',
        'created_at',
    )
    search_fields = ('order',)
    list_filter = ('created_at', 'order',)
    ordering = ('-created_at',)
