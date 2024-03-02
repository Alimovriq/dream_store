from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from products.models import Product


USER = get_user_model()


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
    address = models.TextField(
        max_length=500,
        help_text='Введите адрес доставки',
        verbose_name='Адрес доставки')
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
