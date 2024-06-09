from rest_framework import serializers

from orders.models import OrderRefund, OrderItemsRefund


class OrderItemsRefundSerializer(serializers.ModelSerializer):
    """
    Сериалиазтор для товаров, которые для возарата.
    """

    class Meta:
        model = OrderItemsRefund
        fields = (
            'order_item',
            'quantity',
        )


class OrderRefundSerializer(serializers.ModelSerializer):
    """
    Сериализатор для главной модели возвратов.
    """

    refund_items = serializers.SerializerMethodField()

    class Meta:
        model = OrderRefund
        fields = (
            'order',
            'refund_items',
            'created_at',
            'comment',
            'status',
        )

    def get_refund_items(self, obj):
        order_refund_items = OrderItemsRefund.objects.filter(refund=obj)
        return OrderItemsRefundSerializer(order_refund_items, many=True).data
