from django.contrib import admin

from .models import OrderPayment


@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    """
    Админка для оплаченных Заказов.
    """

    list_display = (
        'idempotence_key',
        'order',
        'payment_id',
        'status',
        'value',
        'created_at',
    )
    search_fields = ('order',)
    list_filter = ('created_at', 'order',)
    ordering = ('-created_at',)
