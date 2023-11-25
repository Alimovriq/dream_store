from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from products.models import Shop_basket
from products.utils import process_shop_basket


class ShopBasketView(GenericAPIView):
    """
    Представление для получения списка корзины
    или ее создания.
    """

    queryset = Shop_basket.objects.all()
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return process_shop_basket(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return process_shop_basket(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return process_shop_basket(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return process_shop_basket(request, *args, **kwargs)
