from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Product, Order, OrderItems


@receiver(pre_save, sender=OrderItems)
def update_product_stock_save(sender, instance, **kwargs) -> None:
    """
    Обновляет итоговую стоимость
    товара при сохранении объекта
    заказов.
    """

    order_item = OrderItems.objects.filter(
        order=instance.order,
        product=instance.product.pk)
    order_obj = Order.objects.filter(
        pk=instance.order.pk).first()
    order_obj.total_price = (
        instance.product.price * int(instance.quantity))

    product_obj = Product.objects.filter(
        pk=instance.product.pk).first()

    if not order_item:
        product_obj.quantity -= instance.quantity
    else:
        product_obj.quantity += order_item.first().quantity
        product_obj.quantity -= instance.quantity

    product_obj.save()
    order_obj.save()


@receiver(pre_delete, sender=OrderItems)
def update_product_stock_del(sender, instance, **kwargs) -> None:
    """
    Обновляет итоговую стоимость
    товара при удалении объекта
    заказов.
    """

    product_obj = Product.objects.filter(
        pk=instance.product.pk).first()
    product_obj.quantity += instance.quantity
    product_obj.save()
