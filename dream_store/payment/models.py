import uuid

from django.db import models

from orders.models import Order


class OrderPayment(models.Model):
    """
    Модель оплаты заказов.
    """

    idempotence_key = models.UUIDField(
        primary_key=True,
        max_length=64,
        default=uuid.uuid4(),
        editable=False,
        verbose_name='Ключ идемпотентности',
        help_text='Ключ идемпотентности'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='payments',
        help_text='id Заказа'
    )
    payment_id = models.CharField(
        verbose_name='id платежа Yookassa',
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text='id платежа от Yookassa'
    )
    status = models.CharField(
        verbose_name='Статус платежа',
        max_length=60,
        default='created',
        help_text='Статус платежа'
    )
    value = models.DecimalField(
        verbose_name='Сумма',
        decimal_places=2,
        max_digits=10,
        blank=True,
        editable=False,
        help_text='Сумма платежа'
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
