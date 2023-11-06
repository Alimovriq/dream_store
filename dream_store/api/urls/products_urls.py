from django.urls import path
from api.views import products_views as views


urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<str:slug>/', views.ProductDetail.as_view()),
    path('products/<str:slug>/add_cart', views.ShopBasketAddItem.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<str:slug>/', views.CategoryDetail.as_view()),
    path('brands/', views.BrandList.as_view()),
    path('brands/<str:slug>/', views.BrandDetail.as_view()),
    path('countries/', views.CountryProductList.as_view()),
    path('countries/<int:pk>/', views.CountryProductDetail.as_view()),
]
