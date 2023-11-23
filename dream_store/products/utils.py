from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from api.serializers.shop_basket_serializers import (
    ShopBasketItemCreateSerializer, ShopBasketUpdateSerializer,)
from .models import Shop_basket, Shop_basket_items

# Функции для работы с корзиной через views для API

USER = get_user_model()


# def get_or_create_shop_basket(request: dict) -> dict:
#     """
#     Создает или находит существующую корзину.
#     Берет данные из request.
#     """

#     customer = request.user
#     shop_basket = Shop_basket.objects.get_or_create(
#         customer=customer)
#     # request.data.update({'shop_basket': shop_basket[0].pk})

#     return shop_basket[0]

def create_shop_basket(customer: str):
    """
    Создает корзину для пользователя.
    """

    created_basket = Shop_basket.objects.create(customer=customer)
    return created_basket


def get_shop_basket(request: dict):
    """
    Позволяет получить объект корзины для пользователя.
    """

    customer = request.user

    if basket := Shop_basket.objects.filter(customer=customer):
        return basket[0]
    return create_shop_basket(customer)


def list_shop_basket(request: dict):
    """
    Возвращет корзину с объектами пользователю.
    """
    
    ...


def destroy_shop_basket(request: dict) -> Response:
    """
    Удаляет корзину, не оставляя в ней товаров пользователя.
    """

    instance = get_shop_basket(request)
    instance.delete()
    return Response(
        {'response': f'Корзина для пользователя {request.user} очищена.'},
        status=status.HTTP_204_NO_CONTENT)


def update_shop_basket(request: dict):
    """
    Обновляет корзину пользователя.
    """

    instance = get_shop_basket(request)
    serializer = ShopBasketUpdateSerializer(
        instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED)
    # return Response(
    #     {'response': f'Корзина для пользователя {request.user} обновлена.'},
    #     status=status.HTTP_201_CREATED)


def process_shop_basket(request: Any,
                        *args: tuple, **kwargs: dict):
    """"
    Инициализирует взаимодействие с корзиной.
    """

    serializer = ShopBasketItemCreateSerializer
    shop_basket = get_shop_basket(request)
    data = {'shop_basket': shop_basket.pk}

    if request.method == 'GET':
        return shop_basket
    elif request.method == 'PUT':
        return update_shop_basket(request)
    elif request.method == 'DELETE':
        return destroy_shop_basket(request)

    # Создание товаров для корзины пользователя.
    if isinstance(request.data, dict):
        request.data.update(data)
        serializer = serializer(data=request.data)
    elif isinstance(request.data, list):
        for ind in range(len(request.data)):
            request.data[ind].update(data)
        serializer = serializer(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

