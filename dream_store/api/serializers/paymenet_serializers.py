from rest_framework import serializers

from payment.models import OrderPayment


class OrderPaymentSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для модели транзакций по заказам.
    """

    # payment_id = serializers.CharField()

    class Meta:
        model = OrderPayment
        fields = (
            'order',
            'payment_id',
            'status',
            'value',
        )
