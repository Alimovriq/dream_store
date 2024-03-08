from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from api.views.utils.order_utils import process_order
from orders.models import Order
from api.serializers.orders_serializers import (
    OrderSerializer, OrderCreateSerializer,)


class OrderList(ListCreateAPIView):
    """
    Представление для получения списка
    и создания заказов пользователя.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return Order.objects.filter(
                customer=self.request.user).order_by(
                    '-created_at')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderSerializer
        elif self.request.method == 'POST':
            return OrderCreateSerializer

    def get(self, request, *args, **kwargs):
        return process_order(
            request, self.get_serializer, self.get_queryset())

    def post(self, request, *args, **kwargs):

        # Если пользователь передает свои товары, то удалить
        if 'products' in request.data.keys():
            del request.data['products']

        return process_order(
            request, self.get_serializer)


class OrderRetrieve(RetrieveAPIView):
    """
    Представление для получения
    конкретного заказа пользователем.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        customer = self.request.user
        return Order.objects.filter(customer=customer)

# Надо переделать верхенее представление так, чтобы оно был на LIST
# Написать еще одну вьюху, которая показывает детаельно, по pk
# На основе этого написать API для payments?
# class OrderPaymentView()
