from django.urls import path
from api.views import products_views as views


urlpatterns = [
    path('products/', views.products_list),
    path('products/<str:slug>/', views.products_detail),
    path('categories/', views.categories_list),
    path('categories/<str:slug>/', views.categories_detail),
]
