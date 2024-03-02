from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from orders.models import Order, OrderItems
from products.models import Product


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
    order_obj.total_price = 0
    if len(order_obj.products.all()) > 0:
        for item in order_obj.products.all():
            if item.name == instance.product.name:
                continue
            else:
                unchanged_order_item = OrderItems.objects.filter(
                    order=order_obj,
                    product=item.pk)
                order_obj.total_price += (
                    item.price * int(unchanged_order_item.first().quantity))

    order_obj.total_price += (
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
    заказов и корректирует склад.
    """

    order_obj = Order.objects.filter(pk=instance.order.pk).first()
    if len(order_obj.products.all()) > 1:
        price_to_delete = instance.product.price * int(instance.quantity)
        order_obj.total_price -= price_to_delete
    else:
        order_obj.total_price = 0
    order_obj.save()

    product_obj = Product.objects.filter(
        pk=instance.product.pk).first()
    product_obj.quantity += instance.quantity
    product_obj.save()
