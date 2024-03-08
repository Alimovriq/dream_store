from django.urls import path

from api.views import orders_views as order

urlpatterns = [
    path('orders/', order.OrderList.as_view()),
    path('orders/<int:pk>/', order.OrderRetrieve.as_view())
]
