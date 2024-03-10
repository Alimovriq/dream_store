import uuid

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from yookassa import Configuration, Payment

from api.serializers.paymenet_serializers import OrderPaymentSerializer
from orders.models import Order


def payment_create(request, order):
    """
    Создание платежа.
    """

    Configuration.account_id = '246787'
    Configuration.secret_key = 'test_XzRZazXj1M-hFtdvMEeiLiNEtvv1Sqm-J1bEYR61p_Y'

    payment = Payment.create({
        "amount": {
            "value": order.total_price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            # "return_url": str(request.get_host())
            # Поменять url
            "return_url": "https://www.example.com/return_url"
        },
        "capture": True,
        "description": f"Заказ № {order.pk} для {order.customer}"
    }, uuid.uuid4())

    return payment


@api_view(['POST'])
def order_payment(request, pk):
    """
    Представление для создания платежа.
    """

    order = get_object_or_404(
        Order,
        customer=request.user,
        pk=pk)

    yookassa_response = payment_create(request, order)

    data = {
        "order": order.pk,
        "payment_id": yookassa_response.id,
        "status": yookassa_response.status,
    }
    serializer = OrderPaymentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            yookassa_response.confirmation,
            status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Проверить оплату и изменить статус платежа в БД!!
