from django.urls import path

from api.views import shop_basket_views as shop_basket

urlpatterns = [
    path('shop_basket/', shop_basket.ShopBasketView.as_view()),
    path(
        'shop_basket/increase/',
        shop_basket.ShopBasketItemIncrease.as_view()),
    path(
        'shop_basket/decrease/',
        shop_basket.ShopBasketItemDecrease.as_view())
    ]
