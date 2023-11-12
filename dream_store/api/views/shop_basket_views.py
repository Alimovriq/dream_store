from rest_framework import permissions, status
from rest_framework.response import Response
from products.models import (
    Shop_basket, Shop_basket_items)
from api.views.mixins import ListCreateUpdateDestroyMixin
from api.serializers.shop_basket_serializers import ShopBasketSerializer
from products.utils import get_shop_basket


class ShopBasketView(ListCreateUpdateDestroyMixin):
    """
    Представление для добавления товара в корзину
    NO -> и его удаления, а также изменения количества.
    """

    queryset = Shop_basket.objects.all()
    serializer_class = ShopBasketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'user': self.request.user,
                'host': self.request.get_host()}

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        shop_basket = get_shop_basket(request)
        serializer = self.get_serializer_class()
        context = self.get_serializer_context()
        return Response(
            serializer(shop_basket,
                       context=context).data,
            status=status.HTTP_200_OK)

    # def get(self, request, *args, **kwargs):
    #     return self.list(
    #         get_or_create_shop_basket(request), *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     updated_request = get_or_create_shop_basket(request)
    #     return self.create(updated_request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     updated_request = get_or_create_shop_basket(request)
    #     return self.update(updated_request, *args, **kwargs)

# class ShopBasketItem(CreateUpdateDestroyMixin):
#     """
#     Представление для добавления товара в корзину
#     NO -> и его удаления, а также изменения количества.
#     """

#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Shop_basket_items
#     serializer_class = ShopBasketItemSerializer

#     def get_serializer_context(self):
#         return {'user': self.request.user,
#                 'product_slug': self.kwargs['slug']}

#     def get_object(self):
#         queryset = Shop_basket_items.objects.filter()
#         return super().get_object()

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)