from django.urls import path
from api.views import products_views as views


urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<str:slug>/', views.ProductDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<str:slug>/', views.CategoryDetail.as_view()),
]
