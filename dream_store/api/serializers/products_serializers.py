from products.models import (
    Products, ProductQuantity,
    Shop_basket, Shop_basket_items,
    Orders, OrderItems,
    Categories)


from rest_framework import serializers


class ProductsSerializer(serializers.Serializer):
    """
    Сериализует данные для товаров.
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=255)
    price = serializers.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     required=True)
    image = serializers.ImageField(required=False)
    description = serializers.CharField(required=False, allow_blank=True,
                                        max_length=500)
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    slug = serializers.SlugField(required=True, max_length=50)
