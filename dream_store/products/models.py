from django.contrib.auth import get_user_model
from django.db import models


USER = get_user_model()


class BasicMetaData(models.Model):
    """
    Базовая модель с мета полями для классов.
    """

    meta_title = models.CharField(
        verbose_name='Мета-название страницы',
        help_text='Мета-название для SEO',
        max_length=255,
        blank=True,
        null=True)
    meta_description = models.CharField(
        verbose_name='Мета-описание страницы',
        help_text='Мета-описание для SEO',
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        abstract = True


class Category(BasicMetaData):
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
        help_text='Добавить изображение',
        null=True,
        blank=True,
        upload_to='categories/')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
        help_text='URL для категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    """
    Модель брендов для товаров.
    """

    name = models.CharField(
        max_length=255,
        help_text='Введите название бренда',
        verbose_name='Бренд')
    description = models.TextField(
        max_length=500,
        help_text='Укажите описание',
        verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
        help_text='URL для бренда')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self) -> str:
        return self.name


class CountryProduct(models.Model):
    """
    Модель для стран.
    """

    name = models.CharField(
        max_length=255,
        help_text='Введите название страны',
        verbose_name='Название страны'
    )

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self) -> str:
        return self.name


class Product(BasicMetaData):
    """
    Модель товаров.
    """

    name = models.CharField(
        max_length=255,
        help_text='Введите название товара',
        verbose_name='Наименование',
        unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        help_text='Укажите стоимость товара',
        verbose_name='Стоимость')
    quantity = models.PositiveIntegerField(
        verbose_name='Количество товара',
        help_text='Укажите количество товара на складе',
        default=0)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        help_text='Выберите бренд',
        verbose_name='Бренд')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        help_text='Выберите категорию',
        verbose_name='Категория')
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Добавить изображние для поста',
        null=True,
        blank=True,
        upload_to='products/')
    description = models.TextField(
        max_length=500,
        blank=True,
        help_text='Введите описание товара',
        verbose_name='Описание')
    country = models.ForeignKey(
        CountryProduct, on_delete=models.CASCADE,
        help_text='Выберите страну производства',
        verbose_name='Страна')
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
        help_text='URL для товара')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return self.name
