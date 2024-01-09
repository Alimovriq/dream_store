
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
# class OrderItemsSerializer(serializers.ModelSerializer):
#     """
#     Сериализует данные для объектов в заказах.
#     """

#     class Meta:
#         model = OrderItems
#         fields = ('order', 'product', 'quantity',)


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
    # products = ProductOrderSerializer(
    #     many=True, source='orderitems_set', required=False)

    class Meta:
        model = Order
        fields = (
            'id', 'customer', 'products', 'total_price',
            'created_at', 'address', 'is_payed',)
        read_only_fields = (
            'id', 'total_price', 'created_at', 'is_payed',)

    def create(self, validated_data):
        # Передать данные пользователя
        # Найти корзину, определить связанные объекты
        # Создать Заказ
        # Связанные объекты перенести в OrderItems
        # Обнулить связанные объекты для корзины пользователя
        # Сохранить изменения.
        customer = validated_data.get('customer')
        if shop_basket := Shop_basket.objects.filter(customer=customer):
            if len(shop_basket.first().products.all()) > 0:
                print(
                    f'shop_basket products {shop_basket.first().products.all()}')
        else:
            raise serializers.ValidationError(
                'У пользователя пустая коризна')
        order_obj = Order.objects.create(customer=customer)
        return order_obj

