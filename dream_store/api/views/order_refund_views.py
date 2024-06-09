from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView

from orders.models import Order, OrderRefund, OrderItemsRefund
from api.serializers.orders_refund_serializers import OrderRefundSerializer


class OrderRefundList(ListCreateAPIView):
    """
    Представление для получения списка
    и создания возвратов для заказов
    пользователя.
    """

    serializer_class = OrderRefundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderRefund.objects.filter(
            order__customer=self.request.user).order_by('-created_at')
