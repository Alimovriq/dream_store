from typing import Any
from rest_framework import status
from rest_framework.response import Response

from products.models import (
    Order, Shop_basket, Shop_basket_items,)


def create_order_items(order_obj: Any, shop_basket_obj: Any) -> dict:
    """
    Создает объекты для заказа пользователя.
    """

    data = {}
    shop_basket_items_obj = Shop_basket_items.objects.filter(
        shop_basket=shop_basket_obj)
    for item in shop_basket_items_obj:
        if 'products' not in data.keys():
            data['products'] = [
                {
                    'order': order_obj.pk,
                    'product': item.product.name,
                    'quantity': item.quantity
                    }
                ]
        else:
            data['products'] += [
                {
                    'order': order_obj.pk,
                    'product': item.product.name,
                    'quantity': item.quantity
                    }
                ]
    return data


def create_order(customer: Any) -> Any:
    """
    Создает и возвращает заказ
    для пользователя.
    """

    Order.objects.create(customer=customer)
    qs = Order.objects.all()
    order_obj = qs[::-1][0]
    return order_obj


def process_order(request: Any, get_serializer: Any) -> Response:
    """
    Проверяет наличие корзины у пользователя
    и создает, либо не создает заказ для пользователя
    с учетом удаления старой корзины.
    """

    # Проверяю наличие корзины пользователя
    customer = request.user

    # Если корзина есть и непустая
    if shop_basket := Shop_basket.objects.filter(customer=customer):
        shop_basket_obj = shop_basket.first()
        if len(shop_basket_obj.products.all()) > 0:

            order_obj = create_order(customer=customer)

            data = create_order_items(order_obj, shop_basket_obj)
            data.update({'customer': customer})
            request.data.update(data)
            serializer = get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
            order_obj.delete()
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {'errors': 'Корзина пользователя пустая'},
        status=status.HTTP_400_BAD_REQUEST)
