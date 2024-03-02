from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from shop_basket.models import Shop_basket
from api.views.utils.shop_basket_utils import (
    process_shop_basket, increase_item_value,
    decrease_item_value,)


class ShopBasketView(GenericAPIView):
    """
    Представление для получения списка объектов корзины,
    создания, изменения и удаления.
    """

    queryset = Shop_basket.objects.all()
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return process_shop_basket(request)

    def post(self, request, *args, **kwargs):
        return process_shop_basket(request)

    def delete(self, request, *args, **kwargs):
        return process_shop_basket(request)

    def put(self, request, *args, **kwargs):
        return process_shop_basket(request)


class ShopBasketItemIncrease(APIView):
    """
    Представление для увеличения количества товара.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return increase_item_value(request)


class ShopBasketItemDecrease(APIView):
    """
    Представление для уменьшения количества товара
    с возможностью удаления объекта, если = 0.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return decrease_item_value(request)
