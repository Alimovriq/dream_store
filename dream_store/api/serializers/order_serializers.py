
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from products.models import (
    Product, Shop_basket, Shop_basket_items, Order, OrderItems,)

USER = get_user_model()


class ProductOrderSerializer(serializers.ModelSerializer):
    """
    Данные товара для заказа пользователя.
    """

    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItems
        fields = ('name', 'quantity',
                  'image', 'slug', 'total_price',)

    def get_name(self, obj):
        return obj.product.name

    def get_image(self, obj):
        # request = self.context.get('host')
        # if obj.product.image:
        #     full_url = request + obj.product.image.url
        #     return full_url
        return 'null'

    def get_slug(self, obj):
        return obj.product.slug

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов Заказа.
    """

    product = serializers.SlugRelatedField(
        slug_field='name', queryset=Product.objects.all())

    class Meta:
        model = OrderItems
        fields = ('order',
                  'product', 'quantity',)
        validators = [
            UniqueTogetherValidator(
                queryset=OrderItems.objects.all(),
                fields=['product', 'order']
            )
        ]


class OrderListSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для получения списка заказов пользователя.
    """

    customer = serializers.SlugRelatedField(
        slug_field='email', read_only=True)
    products = ProductOrderSerializer(
        many=True, source='orderitems_set')

    class Meta:
        model = Order
        fields = (
            'id', 'customer', 'products', 'total_price',
            'created_at', 'address', 'is_payed',)
        read_only_fields = fields


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Сериализует данные для создания заказов пользователя.
    """

    customer = serializers.SlugRelatedField(
        slug_field='email', queryset=USER.objects.all())
    products = OrderItemCreateSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = (
            'id', 'customer', 'products', 'total_price',
            'created_at', 'address', 'is_payed',)
        read_only_fields = (
            'id', 'total_price', 'created_at', 'is_payed',)

    def create(self, validated_data):
        customer = validated_data.get('customer')
        products = validated_data.get('products')
        address = validated_data.get('address')

        for item in products:
            OrderItems.objects.create(
                order=item['order'],
                product=item['product'],
                quantity=item['quantity']
            )

        order_obj = Order.objects.all()[::-1][0]
        order_obj.address = address
        order_obj.save()

        shop_basket_obj = Shop_basket.objects.filter(customer=customer)
        shop_basket_obj.delete()

        # Поменять ответ
        return validated_data
