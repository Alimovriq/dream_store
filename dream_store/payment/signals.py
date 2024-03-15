from django.db.models.signals import pre_save
from django.dispatch import receiver

from orders.models import Order
from payment.models import OrderPayment


@receiver(pre_save, sender=OrderPayment)
def payment_value_save(sender, instance, **kwargs) -> None:
    """
    Передает значение общей суммы заказа
    в модель OrderPayment, меняет is_payed
    заказа (Orders) на True, если соответствует
    "succeeded".
    """

    order_obj = Order.objects.filter(
        pk=instance.order.pk).first()
    instance.value = order_obj.total_price

    if instance.status == "succeeded":
        order_obj.is_payed = True
        order_obj.save()
