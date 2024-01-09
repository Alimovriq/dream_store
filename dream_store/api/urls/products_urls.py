from django.urls import path
from api.views import products_views as product
from api.views import shop_basket_views as shop_basket
from api.views import order_views as order


urlpatterns = [
    path('products/', product.ProductList.as_view()),
    path('products/<str:slug>/', product.ProductDetail.as_view()),
    path('shop_basket/', shop_basket.ShopBasketView.as_view()),
    path('shop_basket/increase/',
         shop_basket.ShopBasketItemIncrease.as_view()),
    path('shop_basket/decrease/',
         shop_basket.ShopBasketItemDecrease.as_view()),
    path('orders/', order.OrderView.as_view()),
    path('categories/', product.CategoryList.as_view()),
    path('categories/<str:slug>/', product.CategoryDetail.as_view()),
    path('brands/', product.BrandList.as_view()),
    path('brands/<str:slug>/', product.BrandDetail.as_view()),
    path('countries/', product.CountryProductList.as_view()),
    path('countries/<int:pk>/', product.CountryProductDetail.as_view()),
]
