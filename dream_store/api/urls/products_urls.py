from django.urls import path
from api.views import products_views as views


urlpatterns = [
    path('products/', views.products_list)
]
