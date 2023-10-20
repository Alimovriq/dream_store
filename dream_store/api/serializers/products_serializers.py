import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from products.models import (
    Products, ProductQuantity,
    Shop_basket, Shop_basket_items,
    Orders, OrderItems,
    Categories)


class Base64ImageField(serializers.ImageField):
    """
    Кастомный сериализатор для декодирования изображений.
    """

    def to_internal_value(self, data):
        """
        Метод работает при поступлении запроса.
        """

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class ProductsSerializer(serializers.Serializer):
    """
    Сериализует данные для товаров.
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=255)
    price = serializers.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     required=True)
    image = Base64ImageField(required=False)
    description = serializers.CharField(required=False, allow_blank=True,
                                        max_length=500)
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field='name')
    slug = serializers.SlugField(required=True, max_length=50)

    def create(self, validated_data):
        """
        Метод для создания и возврата объекта экземпляра от
        входящих данных.
        """

        return Products.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Метод для обновления и возврата объекта экземпляра от
        входящих данных
        """

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.category = validated_data.get(
            'category', instance.category)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance
