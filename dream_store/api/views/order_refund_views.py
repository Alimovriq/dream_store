from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from orders.models import Order, OrderRefund, OrderItemsRefund
from api.serializers.orders_refund_serializers import (
    OrderRefundSerializer, OrderItemsRefundSerializerCreate,)


class OrderRefundListCreateView(ListCreateAPIView):
    """
    Представление для получения списка
    всех возвратов для заказов пользователя.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderRefund.objects.filter(
            order__customer=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderRefundSerializer
        return OrderItemsRefundSerializerCreate

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class OrderItemRefundDetail(RetrieveDestroyAPIView):
    """
    Представление для получения конкретного
    возарата по <pk>, либо его удаления.
    """

    queryset = OrderRefund.objects.all()
    serializer_class = OrderRefundSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
