from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from products.models import Product


USER = get_user_model()


class Shop_basket(models.Model):
    """
    Общая модель корзины для товаров.
    """

    products = models.ManyToManyField(
        Product,
        through='Shop_basket_items',
        help_text='Выберите товар',
        verbose_name='Товары')
    customer = models.OneToOneField(
        USER,
        on_delete=models.CASCADE,
        help_text='Укажите пользователя(Покупатель)',
        verbose_name='Покупатель')

    class Meta:
        verbose_name = 'Корзина с товарами'
        verbose_name_plural = 'Корзины с товарами'

    def __str__(self) -> str:
        return f'Корзина для {self.customer}'


class Shop_basket_items(models.Model):
    """
    Товары для корзины.
    """

    shop_basket = models.ForeignKey(
        Shop_basket,
        on_delete=models.CASCADE,
        help_text='Выберите корзину',
        verbose_name='Корзина')
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
        verbose_name = 'Товар для корзины'
        verbose_name_plural = 'Товары для корзин'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'shop_basket'],
                name='unique_product_shop_basket'
            )
        ]

    def __str__(self) -> str:
        return f'Объект корзины с {self.product} в кол-ве {self.quantity} ед.'

    def clean(self):
        """
        Проверка на количество товара на складе.
        """

        queryset = Product.objects.filter(id=self.product.id)
        if self.quantity > queryset.first().quantity:
            raise ValidationError(
                f'Недостаточное количество товара {self.product.name} в наличии.')
