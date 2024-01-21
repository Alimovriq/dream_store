from rest_framework import permissions
from rest_framework.generics import GenericAPIView

from api.views.utils.order_utils import process_order
from products.models import Order
from api.serializers.order_serializers import (
    OrderListSerializer, OrderCreateSerializer,)


class OrderView(GenericAPIView):
    """
    Представление для получения списка
    и создания заказов пользователя.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.method == 'GET':
            return Order.objects.filter(customer=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        elif self.request.method == 'POST':
            return OrderCreateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        # Если пользователь передает свои товары, то удалить
        if 'products' in request.data.keys():
            del request.data['products']

        return process_order(request, self.get_serializer)
