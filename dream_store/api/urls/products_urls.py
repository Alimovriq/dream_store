from django.urls import path
from api.views import products_views as views
from api.views import shop_basket_views as cart_views


urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<str:slug>/', views.ProductDetail.as_view()),
    path('shop_cart/', cart_views.ShopBasketView.as_view()),
    # path('products/<str:slug>/shop_cart', views.ShopBasketItem.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<str:slug>/', views.CategoryDetail.as_view()),
    path('brands/', views.BrandList.as_view()),
    path('brands/<str:slug>/', views.BrandDetail.as_view()),
    path('countries/', views.CountryProductList.as_view()),
    path('countries/<int:pk>/', views.CountryProductDetail.as_view()),
]
