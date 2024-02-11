from typing import Any
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from api.serializers.shop_basket_serializers import (
    ShopBasketItemCreateSerializer, ShopBasketUpdateSerializer,
    ShopBasketSerializer, ShopBasketItemIncreaseSerializer,
    ShopBasketItemDecreaseSerializer,)
from products.models import Shop_basket

# Функции для работы с корзиной через views для API


def create_shop_basket(customer: str):
    """
    Создает корзину для пользователя.
    """

    created_basket = Shop_basket.objects.create(customer=customer)
    return created_basket


def get_shop_basket(request: Any):
    """
    Позволяет получить объект корзины для пользователя.
    """

    customer = request.user

    if basket := Shop_basket.objects.filter(customer=customer):
        return basket[0]
    return create_shop_basket(customer)


def list_shop_basket(request: Any) -> Response:
    """
    Возвращет корзину с объектами пользователю.
    """

    context = {'host': request.get_host()}
    serializer = ShopBasketSerializer
    shop_basket = get_shop_basket(request)
    return Response(
        serializer(shop_basket, context=context).data,
        status=status.HTTP_200_OK)


def destroy_shop_basket(request: Any) -> Response:
    """
    Удаляет корзину, не оставляя в ней товаров пользователя.
    """

    instance = get_shop_basket(request)
    instance.delete()
    return Response(
        {'response': f'Корзина для пользователя {request.user} очищена.'},
        status=status.HTTP_204_NO_CONTENT)


def update_shop_basket(request: Any) -> Response:
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


def create_shopbasket_item(request: Any) -> Response:
    """
    Добавляет товары в корзину пользователя.
    Возможно добавлять по одному товару,
    либо списком.
    """

    serializer = ShopBasketItemCreateSerializer
    shop_basket = get_shop_basket(request)
    data = {'shop_basket': shop_basket.pk}

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


def process_shop_basket(request: Any) -> Response:
    """
    Инициализирует взаимодействие с корзиной.
    Поиск, либо создание корзины пользователя, с
    последующим ответом, включающий данные объекта.
    Очищение корзины пользователя, обновление товаров
    или частичное удаление.
    """

    if request.method in SAFE_METHODS:
        return list_shop_basket(request)
    elif request.method == 'POST':
        return create_shopbasket_item(request)
    elif request.method == 'PUT':
        return update_shop_basket(request)
    elif request.method == 'DELETE':
        return destroy_shop_basket(request)


def increase_item_value(request: Any) -> Response:
    """
    Увеличивает количество товара в корзине.
    """

    serializer = ShopBasketItemIncreaseSerializer
    shop_basket = get_shop_basket(request)
    request.data.update({'shop_basket': shop_basket.pk})
    serializer = serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        f' Количество {request.data["product"]} увеличено на 1 ед.',
        status=status.HTTP_201_CREATED)


def decrease_item_value(request: Any) -> Response:
    """
    Уменьшает количество товара в корзине.
    """

    serializer = ShopBasketItemDecreaseSerializer
    shop_basket = get_shop_basket(request)
    request.data.update({'shop_basket': shop_basket.pk})
    serializer = serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        f'Количество {request.data["product"]} уменьшено на 1 ед.',
        status=status.HTTP_201_CREATED)
