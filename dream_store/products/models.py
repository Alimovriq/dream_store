from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


USER = get_user_model()


class BasicMetaData(models.Model):
    """
    Базовая модель с мета полями для классов.
    """

    meta_title = models.CharField(
        verbose_name='Мета-название страницы',
        max_length=255,
        blank=True,
        null=True)
    meta_description = models.CharField(
        verbose_name='Мета-описание страницы',
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        abstract = True


class Categories(BasicMetaData):
    """
    Категории для товаров.
    """

    name = models.CharField(
        max_length=255,
        help_text='Введите название категории',
        verbose_name='Название')
    description = models.CharField(
        max_length=255,
        help_text='Введите описание категории',
        blank=True,
        verbose_name='Описание')
    image = models.ImageField(
        verbose_name='Изображение',
        null=True,
        blank=True,
        upload_to='categories/')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Products(BasicMetaData):
    """
    Модель товаров.
    """

    name = models.CharField(
        max_length=255,
        help_text='Введите название товара',
        verbose_name='Наименование')
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=1,
        help_text='Укажите стоимость товара',
        verbose_name='Стоимость')
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        help_text='Выберите категорию',
        verbose_name='Категория')
    image = models.ImageField(
        verbose_name='Изображение',
        null=True,
        blank=True,
        upload_to='products/')
    description = models.TextField(
        max_length=500,
        blank=True,
        help_text='Введите описание товара',
        verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return self.name


class ProductQuantity(models.Model):
    """
    Модель количества товаров.
    """

    product = models.ForeignKey(
                Products,
                on_delete=models.CASCADE,
                help_text='Выберите товар',
                verbose_name='Товар')
    stock = models.PositiveIntegerField(
        verbose_name='Доступно на складе',
        help_text='Укажите количество товара на складе',)

    class Meta:
        verbose_name = 'Количество доступного товара'
        verbose_name_plural = 'Количество доступных товаров'

    def __str__(self) -> str:
        return f'{self.product} доступно для заказа {self.stock} ед.'


class Shop_basket(models.Model):
    """
    Общая модель корзины для товаров.
    """

    products = models.ManyToManyField(
        Products,
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
        Products,
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

    def __str__(self) -> str:
        return f'Объект корзины с {self.product} в кол-ве {self.quantity} ед.'

    def clean(self):
        """
        Проверка на количество товара на складе.
        """

        queryset = ProductQuantity.objects.filter(product=self.product)
        if self.quantity > queryset.first().stock:
            raise ValidationError(
                f'Недостаточное количество товара {self.product.name} в наличии.')


class Orders(models.Model):
    """
    Общая модель для заказов.
    """

    customer = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        help_text='Выберите пользователя(Покупатель)',
        verbose_name='Покупатель')
    products = models.ManyToManyField(
        Products,
        through='OrderItems',
        help_text='Выберите товар',
        verbose_name='Товары')
    total_price = models.DecimalField(
        max_digits=6,
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
        Orders,
        on_delete=models.CASCADE,
        help_text='Выберите заказ',
        verbose_name='Заказ')
    product = models.ForeignKey(
        Products,
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

    def __str__(self) -> str:
        return f'{self.product.name} ({self.quantity})'

    def clean(self):
        """
        Проверка на количество товара на складе.
        """

        queryset = ProductQuantity.objects.filter(product=self.product)
        if self.quantity > queryset.first().stock:
            raise ValidationError(
                f'Недостаточное количество товара {self.product.name} в наличии.')

    def save(self, *args, **kwargs):
        """
        Обновление итоговой стоимости заказа и вычитание кол-ва со склада.
        """

        if self.order:
            queryset_order = Orders.objects.filter(pk=self.order.pk)
            queryset_product_quantity = ProductQuantity.objects.filter(
                product=self.product)
            order_obj = queryset_order.first()
            order_obj.total_price += (
                self.product.price * self.quantity)
            if queryset_product_quantity:
                # Если найден кьюрисет в модели ProductQuantity,
                # то убавляем кол-во
                product_quantity_obj = queryset_product_quantity.first()
                product_quantity_obj.stock -= self.quantity
                product_quantity_obj.save()
            order_obj.save()
        return super().save(*args, **kwargs)
