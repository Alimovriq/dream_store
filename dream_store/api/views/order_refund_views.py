from django.core.exceptions import ValidationError as DjangoError
from rest_framework import permissions, status
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from orders.models import Order, OrderRefund
from api.serializers.orders_refund_serializers import (
    OrderRefundSerializer, OrderRefundSerializerCreate,)


class OrderRefundListCreateView(ListCreateAPIView):
    """
    Представление для получения списка
    всех возвратов, либо создания одного.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderRefund.objects.filter(
            order__customer=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderRefundSerializer
        return OrderRefundSerializerCreate

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        """
        Для перехвата ошибки на уровне валидации модели.
        """

        try:
            # super().create(request, *args, **kwargs)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED, headers=headers)
        except DjangoError as e:
            return Response({'detail': e}, status.HTTP_400_BAD_REQUEST)


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
