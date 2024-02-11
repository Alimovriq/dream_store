import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from products.models import (
    Product, Brand, CountryProduct, Category,)


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
