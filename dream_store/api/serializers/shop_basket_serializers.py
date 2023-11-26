from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from products.models import (
    Product, Shop_basket, Shop_basket_items,)


class ProductShopBasketListSerializer(serializers.ModelSerializer):
    """
    Данные товара для корзины пользователя.
    """

    name = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Shop_basket_items
        fields = ('name', 'quantity',
                  'image', 'slug', 'total_price',)

    def get_name(self, obj):
        return obj.product.name

    def get_quantity(self, obj):
        return obj.quantity

    def get_image(self, obj):
        request = self.context.get('host')
        if obj.product.image:
            full_url = request + obj.product.image.url
            return full_url
        return 'null'

    def get_slug(self, obj):
        return obj.product.slug

    def get_total_price(self, obj):
        return obj.product.price * self.get_quantity(obj)


class ProductShopBasketUpdateSerializer(serializers.ModelSerializer):
    """
    Данные товара для обновления корзины пользователя.
    """

    product = serializers.SlugRelatedField(
        slug_field='name', queryset=Product.objects.all())

    class Meta:
        model = Shop_basket_items
        fields = ('product', 'quantity',)


class ShopBasketSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения корзины с товарами пользователя.
    """

    products = ProductShopBasketListSerializer(
        many=True, source='shop_basket_items_set')
    total_basket_price = serializers.SerializerMethodField()
    total_quantity_of_products = serializers.SerializerMethodField()

    class Meta:
        model = Shop_basket
        fields = ('id', 'products',
                  'total_basket_price',
                  'total_quantity_of_products',)

    def get_total_basket_price(self, obj):
        """
        Высчитывает общую стоимость товаров в корзине.
        """

        total_basket_price = 0
        shop_basket_items = Shop_basket_items.objects.filter(
            shop_basket=obj)
        for item in shop_basket_items:
            total_basket_price += item.quantity * item.product.price
        return total_basket_price

    def get_total_quantity_of_products(self, obj):
        """
        Высчитывает общее количество товаров в корзине.
        """

        total_quantity_of_products = 0
        shop_basket_items = Shop_basket_items.objects.filter(
            shop_basket=obj)
        for item in shop_basket_items:
            total_quantity_of_products += item.quantity
        return total_quantity_of_products


class ShopBasketItemCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объектов корзины.
    """

    product = serializers.SlugRelatedField(
        slug_field='name', queryset=Product.objects.all())

    class Meta:
        model = Shop_basket_items
        fields = ('shop_basket',
                  'product', 'quantity',)
        validators = [
            UniqueTogetherValidator(
                queryset=Shop_basket_items.objects.all(),
                fields=['product', 'shop_basket']
            )
        ]


class ShopBasketItemIncreaseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для увеличения количества объекта корзины.
    """

    product = serializers.SlugRelatedField(
        slug_field='name', queryset=Product.objects.all())

    class Meta:
        model = Shop_basket_items
        fields = ('shop_basket',
                  'product',)

    def create(self, validated_data):
        shop_basket = validated_data['shop_basket']
        product = validated_data['product']
        item = Shop_basket_items.objects.filter(
            shop_basket=shop_basket, product=product).first()
        item.quantity += 1
        item.save()
        return item

    def validate(self, value):
        shop_basket = value['shop_basket']
        product = value['product']

        if not Shop_basket_items.objects.filter(
            shop_basket=shop_basket, product=product
        ):
            raise serializers.ValidationError(
                f'Товар {value["product"]} отсутствует в корзине'
            )
        return value


class ShopBasketItemDecreaseSerializer(ShopBasketItemIncreaseSerializer):
    """
    Сериализатор для уменьшения количества объекта корзины.
    """

    def create(self, validated_data):
        shop_basket = validated_data['shop_basket']
        product = validated_data['product']
        item = Shop_basket_items.objects.filter(
            shop_basket=shop_basket, product=product).first()
        item.quantity -= 1
        if item.quantity == 0:
            item.delete()
        else:
            item.save()
        return item


class ShopBasketUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления корзины с товарами пользователя.
    """

    products = ProductShopBasketUpdateSerializer(
        many=True, source='shop_basket_items_set')

    class Meta:
        model = Shop_basket
        fields = ('products',)

    def update(self, instance, validated_data):
        for key in validated_data['shop_basket_items_set']:
            if shop_basket_item := Shop_basket_items.objects.filter(
                    shop_basket=instance, product=key['product']):
                if key['quantity'] > 0:
                    shop_basket_item[0].quantity = key['quantity']
                    shop_basket_item[0].save()
                elif key['quantity'] == 0:
                    shop_basket_item.delete()
                elif key['quantity'] < 0:
                    raise serializers.ValidationError({
                        'quantity': 'Данное поле должно быть больше >= 0.'
                    })
        return instance
