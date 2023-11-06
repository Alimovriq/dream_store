import base64

from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from rest_framework import serializers

from users.models import User
from products.models import (
    Product, Shop_basket, Shop_basket_items,
    Order, OrderItems, Brand,
    CountryProduct, Category,)


class Base64ImageField(serializers.ImageField):
    """
    Кастомный сериализатор для декодирования изображений.
    """

    def to_internal_value(self, data):
        """
        Проверяет, что поступивший запрос соответствует
        для декадирования изображения.
        Метод работает при поступлении запроса.
        """

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализует данные для категорий без мета-данных.
    """

    image = Base64ImageField(required=False)
    total_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'description',
            'image', 'slug', 'total_products',)

    def get_total_products(self, obj):
        """
        Поле с общим количеством товаров в данной категории.
        """

        products = Product.objects.filter(category=obj.id)
        return products.count()


class CategoryDetailSerializer(CategorySerializer):
    """
    Сериализует данные для категорий с мета-данными.
    """

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'description',
            'image', 'slug', 'total_products',
            'meta_title', 'meta_description',)


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для товаров.
    """

    brand = serializers.SlugRelatedField(
        queryset=Brand.objects.all(), slug_field='name')
    country = serializers.SlugRelatedField(
        queryset=CountryProduct.objects.all(), slug_field='name')
    image = Base64ImageField(required=False)
    description = serializers.CharField(required=False, allow_blank=True,
                                        max_length=500)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='name')

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'price', 'quantity',
            'brand', 'country', 'image',
            'description', 'category', 'slug',
        )


class ProductDetailSerializer(ProductSerializer):
    """
    Сериализатор для товаров
    поле "category" - подробное.
    """

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'price', 'quantity',
            'brand', 'country', 'image',
            'description', 'category', 'slug',
            'meta_title', 'meta_description',
        )


class BrandSerializer(serializers.ModelSerializer):
    """
    Сериалзует данные для брендов.
    """

    class Meta:
        model = Brand
        fields = (
            'id', 'name',
            'description', 'slug')


class CountryProductSerializer(serializers.ModelSerializer):
    """
    Сериалзует данные для стран.
    """

    class Meta:
        model = CountryProduct
        fields = ('id', 'name',)


class ShopBasketSerializer(serializers.ModelSerializer):
    """
    ...
    """

    class Meta:
        model = Shop_basket
        fields = ('id', 'products', 'customer',)


class ShopBasketItemsSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для добавления товаров в корзину.
    Проверяет наличие корзины для юзера и добавляет товар.
    """

    def save(self, **kwargs):
        product = Product.objects.filter(
            slug=self.context['product_slug']).first()
        user = self.context['user']
        shop_basket = Shop_basket.objects.get_or_create(customer=user)
        shop_basket_item = Shop_basket_items.objects.get_or_create(
            shop_basket=shop_basket[0], product=product
        )
        if 'quantity' in self.validated_data:
            quantity = self.validated_data['quantity']
            if quantity == 0:
                quantity = 1
            shop_basket_item[0].quantity += quantity
        else:
            shop_basket_item[0].quantity += 1
        shop_basket_item[0].save()
        self.instance = shop_basket_item[0]

        return self.instance

    def validate(self, value):
        product = Product.objects.filter(
            slug=self.context['product_slug']).first()
        if "quantity" in value:
            if value['quantity'] <= 0:
                raise serializers.ValidationError(
                    'Количество товара должно быть больше 0')
            if value['quantity'] > product.quantity:
                raise serializers.ValidationError(
                    'Количество товара больше, чем в наличии на складе.')
        return value

    class Meta:
        model = Shop_basket_items
        fields = ('id', 'quantity',)
