from typing import Any
from rest_framework import status
from rest_framework.response import Response

from orders.models import Order
from shop_basket.models import Shop_basket, Shop_basket_items


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

    print('STARTED')
    Order.objects.create(customer=customer)
    qs = Order.objects.all()
    order_obj = qs[::-1][0]
    return order_obj


def post_operations_in_orders(request: Any, serializer: Any) -> Response:
    """
    Операции с заказами при POST запросах.
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
            serializer = serializer(data=request.data)
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


def get_operations_in_orders(
        request: Any, serializer: Any, queryset: Any) -> Response:
    """
    Операции с заказами при GET запросах.
    """

    context = {'host': request.get_host()}
    serializer = serializer(queryset, many=True, context=context)
    if len(queryset) == 0:
        return Response(
            {'detail': 'Заказы отсутствуют'}, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_200_OK)


def process_order(request: Any, serializer: Any, queryset=None) -> Response:
    """
    Проверяет наличие корзины у пользователя
    и создает, либо не создает заказ для пользователя
    с учетом удаления старой корзины.
    """

    if request.method == 'POST':
        return post_operations_in_orders(request, serializer)
    return get_operations_in_orders(request, serializer, queryset)
