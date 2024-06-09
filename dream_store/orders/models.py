from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from products.models import Product


USER = get_user_model()

CHOICES = (
    ('ACTIVE', 'Активный'),
    ('FINISHED', 'Завершенный'),
    ('CANCELLED', 'Отмененный')
)

# class OrderItemsRefund(models.Model):
#     """
#     Модель с конкретными позициями
#     для отказа в Заказе.
#     """

#     # CHOICES = (
#     #     ('APPPROVED', 'Согласовано'),
#     #     ('CANCELLED', 'Отказано')
#     # )

#     order_item = models.ForeignKey(
#         'OrderItems',
#         on_delete=models.CASCADE,
#         verbose_name='Возвращаемый товар',
#         related_name='refunds',
#         help_text='id товара в Заказе'
#     )
#     refund = models.ForeignKey(
#         'OrderRefund',
#         on_delete=models.CASCADE,
#         verbose_name='Возврат',
#         related_name='orderitemsrefunds',
#         help_text='id возвращаемого Заказа'
#     )
#     quantity = models.PositiveBigIntegerField(
#         verbose_name='Количество',
#         help_text='Количество'
#     )

#     class Meta:
#         verbose_name = 'Возвращаемый товар'
#         verbose_name_plural = 'Возвращаемые товары'

#     def __str__(self) -> str:
#         return f'Вовзарат {self.order_item.product.name} - {self.quantity}'


# class OrderRefund(models.Model):
#     """
#     Модель для отказа от Заказа (возврат).
#     """

#     order = models.ForeignKey(
#         'Order',
#         on_delete=models.CASCADE,
#         verbose_name='Заказ',
#         help_text='id Заказа',
#         related_name='refunds'
#     )
#     created_at = models.DateTimeField(
#         verbose_name='Дата создания',
#         auto_now_add=True,
#         help_text='Дата создания'
#     )
#     comment = models.TextField(
#         verbose_name='Комментарий',
#         blank=True,
#         null=True,
#         help_text='текст для комментария'
#     )

#     class Meta:
#         verbose_name = 'Возврат'
#         verbose_name_plural = 'Возвраты'

#     def __str__(self) -> str:
#         return f'Возврат № {self.pk}'


class Order(models.Model):
    """
    Общая модель для заказов.
    """

    customer = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        help_text='Выберите пользователя(Покупатель)',
        verbose_name='Покупатель')
    products = models.ManyToManyField(
        Product,
        through='OrderItems',
        help_text='Выберите товар',
        verbose_name='Товары')
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Укажите итоговую стоимость',
        verbose_name='Итоговая стоимость')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата заказа')
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=14,
        help_text='Телефон, формат: 79687773366')
    email = models.EmailField(
        verbose_name='Email',
        help_text='Укажите Email')
    comment = models.TextField(
        max_length=500,
        verbose_name='Комментарий',
        help_text='Введите комментарий')
    address = models.TextField(
        max_length=500,
        help_text='Введите адрес доставки',
        verbose_name='Адрес доставки')
    status = models.CharField(
        verbose_name='Статус Заказа',
        choices=CHOICES,
        default=CHOICES[0][0],
        max_length=300)
    is_payed = models.BooleanField(
        default=False,
        help_text='Укажите статус оплаты',
        verbose_name='Статус оплаты')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return f'Заказ № {self.pk}'


class OrderItems(models.Model):
    """
    Объекты для модели заказов.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        help_text='Выберите заказ',
        verbose_name='Заказ')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text='Выберите товар',
        verbose_name='Товар')
    quantity = models.PositiveIntegerField(
        default=1,
        help_text='Укажите количество',
        verbose_name='Количество')

    class Meta:
        verbose_name = 'Товары для заказа'
        verbose_name_plural = 'Товары для заказов'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'order'],
                name='unique_product_order'
            )
        ]

    def __str__(self) -> str:
        return f'{self.product.name} ({self.quantity})'

    def clean(self):
        """
        Проверка на количество товара на складе.
        """

        queryset = Product.objects.filter(pk=self.product.pk)
        if self.quantity > queryset.first().quantity:
            raise ValidationError(
                f'Недостаточное количество товара {self.product.name} в наличии.')


class OrderRefund(models.Model):
    """
    Модель для отказа от Заказа (возврат).
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        help_text='id Заказа',
        related_name='refunds'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        help_text='Дата создания'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        null=True,
        help_text='текст для комментария'
    )
    status = models.CharField(
        verbose_name='Статус возврата',
        choices=CHOICES,
        default=CHOICES[0][0],
        max_length=300)

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'

    def __str__(self) -> str:
        return f'Возврат № {self.pk}'


class OrderItemsRefund(models.Model):
    """
    Модель с конкретными позициями
    для отказа в Заказе.
    """

    refund = models.ForeignKey(
        OrderRefund,
        on_delete=models.CASCADE,
        verbose_name='Возврат',
        related_name='orderitemsrefunds',
        help_text='id возвращаемого Заказа'
    )
    order_item = models.ForeignKey(
        OrderItems,
        on_delete=models.CASCADE,
        # Ограничить выбор товаров == заказ
        # limit_choices_to={
        #     'order': models.F('order__refunds')
        # },
        verbose_name='Возвращаемый товар',
        # related_name='refunds',
        help_text='id товара в Заказе',
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='Количество',
        help_text='Количество',
    )

    class Meta:
        verbose_name = 'Возвращаемый товар'
        verbose_name_plural = 'Возвращаемые товары'

    def __str__(self) -> str:
        return f'Возварат {self.order_item.product.name} - {self.quantity}'

    def clean(self):
        """
        Проверка на количество товара на в заказе.
        """

        if self.order_item.order != self.refund.order:
            raise ValidationError(
                'Вы не можете возвратить товар из другого заказа')

        if self.quantity > self.order_item.quantity:
            raise ValidationError(
                'Количество возвращаемого товара не может быть больше купленного')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
