import uuid

from django.db import models

from orders.models import Order


class OrderPaymenet(models.Model):
    """
    Модель оплат заказов.
    """

    idempotentence_key = models.UUIDField(
        primary_key=True,
        max_length=64,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Ключ идемпотентности',
        help_text='Ключ идемпотентности'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        help_text='id Заказа'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата создания'
    )

    class Meta:
        verbose_name = 'Оплаченный заказ'
        verbose_name_plural = 'Оплаченные заказы'

    def __str__(self) -> str:
        return f'Оплата заказа {self.order.pk}'
