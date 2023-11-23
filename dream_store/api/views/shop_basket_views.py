from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from products.models import (
    Shop_basket, Shop_basket_items)
from api.serializers.shop_basket_serializers import (
    ShopBasketSerializer, ShopBasketItemCreateSerializer,)
from products.utils import process_shop_basket


class ShopBasketView(GenericAPIView):
    """
    Представление для получения списка корзины
    или ее создания.
    """

    queryset = Shop_basket.objects.all()
    # serializer_class = ShopBasketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ShopBasketItemCreateSerializer
        # elif self.request.method == 'PUT':
        #     return ShopBasketItemUpdateSerializer
        elif self.request.method == 'GET':
            return ShopBasketSerializer

    def get_serializer_context(self):
        return {'user': self.request.user,
                'host': self.request.get_host()}

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return process_shop_basket(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return process_shop_basket(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return process_shop_basket(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        shop_basket = process_shop_basket(request)
        serializer = self.get_serializer_class()
        context = self.get_serializer_context()
        # Найти применение контексту
        return Response(
            serializer(shop_basket,
                       context=context).data,
            status=status.HTTP_200_OK)
