from django.contrib.auth import get_user_model
from .models import Shop_basket, Shop_basket_items

# Функции для работы с корзиной через views для API

USER = get_user_model()


def get_or_create_shop_basket(request: dict) -> dict:
    """
    Создает или находит существующую корзину.
    Берет данные из request.
    """

    customer = request.user
    shop_basket = Shop_basket.objects.get_or_create(
        customer=customer)
    request.data.update({'shop_basket': shop_basket[0].pk})

    return request
