from django.urls import path

from api.views import orders_views as order

urlpatterns = [
    path('orders/', order.OrderView.as_view())
]
