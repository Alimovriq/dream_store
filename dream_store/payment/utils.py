from yookassa import Payment

from orders.models import Order
from payment.models import OrderPayment


def check_payment(**kwargs: dict) -> None:
    """
    Проверяет статус платежа заказа
    пользователя, при попытке запроса
    конкретного заказа, если у него статус
    не равен "succeeded" и меняет статус
    заказа на соответствующий Yookassa.
    """

    order = Order.objects.filter(pk=kwargs.get('pk')).first()
    if order_payment := OrderPayment.objects.filter(order=order).first():
        payment_id = order_payment.payment_id
        current_status = order_payment.status
        yookassa_payment = Payment.find_one(payment_id)
        yookassa_payment_status = yookassa_payment['status']
        if current_status != yookassa_payment_status:
            order_payment.status = yookassa_payment_status
            order_payment.save()
