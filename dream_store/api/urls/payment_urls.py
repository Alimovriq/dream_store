from django.urls import path

from api.views.payment_views import order_payment


urlpatterns = [
    path('orders/<int:pk>/payment/', order_payment),
]
