from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from products.models import Order, OrderItems
from api.serializers.order_serializers import (
    OrderListSerializer, OrderCreateSerializer,)


class OrderView(ListCreateAPIView):
    """
    Представление для получения списка
    и создания заказов пользователя.
    """

    # queryset = Order.objects.all()
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
        # В сериализаторе не вызывается метод CREATE!!!!
        customer = self.request.user
        data = {'customer': customer}
        request.data.update(data)
        serializer = self.get_serializer(data=request.data)
        # serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     customer = self.request.user
    #     return serializer.save(customer=customer)
