from django.urls import path

from api.views import order_refund_views as order_refund


urlpatterns = [
    path('orders/refunds/', order_refund.OrderRefundList.as_view()),
]
