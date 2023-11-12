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


class ShopBasketSerializer(serializers.ModelSerializer):
    """
    Сериализатор для корзины товаров пользователя.
    """

    products = ProductShopBasketListSerializer(
        many=True, source='shop_basket_items_set')
    total_basket_price = serializers.SerializerMethodField()

    class Meta:
        model = Shop_basket
        fields = ('id', 'products',
                  'total_basket_price')

    def get_total_basket_price(self, obj):
        total_basket_price = 0
        shop_basket_items = Shop_basket_items.objects.filter(
            shop_basket=obj)
        for item in shop_basket_items:
            total_basket_price += item.quantity * item.product.price
        return total_basket_price


# # Ниже написан неверный сериализатор
# class ShopBasketItemSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Shop_basket_items
#         fields = ('id', 'shop_basket', 'product', 'quantity',)
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Shop_basket_items.objects.all(),
#                 fields=['product', 'shop_basket']
#             )
#         ]

#     def validate(self, value):
#         if 'quantity' in value:
#             product = Product.objects.filter(pk=value['product'].pk)
#             if value['quantity'] <= 0:
#                 raise serializers.ValidationError(
#                     'Количество товара для заказа должно быть больше 0.'
#                 )
#             elif value['quantity'] > product.first().quantity:
#                 raise serializers.ValidationError(
#                     'Количество товара больше, чем доступно для заказа.'
#                 )
#         return value

    # def create(self, validated_data):
    #     print(f' VALIDATED_DATA {validated_data}')
    #     # product = self.validated_data.pop('product')
    #     user = self.context['user']
    #     shop_basket = Shop_basket.objects.get_or_create(customer=user)
    #     shop_basket_item = Shop_basket_items.objects.create(
    #         shop_basket=shop_basket[0], **validated_data
    #     )

    #     return shop_basket_item

    # def save(self, **kwargs):
    #     print('BEGIN!!!')
    #     print(f'PRODUCT {self.validated_data["product"]}')
    #     # product = Product.objects.filter(
    #     #     slug=self.validated_data['product']).first()
    #     product = Product.objects.get(self.validated_data['product'])
    #     print(f'PRODUCT {product}')
    #     user = self.context['user']
    #     shop_basket = Shop_basket.objects.get_or_create(customer=user)
    #     shop_basket_item = Shop_basket_items.objects.get_or_create(
    #         shop_basket=shop_basket[0], product=product
    #     )
    #     if 'quantity' in self.validated_data:
    #         quantity = self.validated_data['quantity']
    #         if quantity == 0:
    #             quantity = 1
    #         shop_basket_item[0].quantity += quantity
    #     else:
    #         shop_basket_item[0].quantity += 1
    #     shop_basket_item[0].save()
    #     self.instance = shop_basket_item[0]

    #     return self.instance

# class ShopBasketItemSerializer(serializers.ModelSerializer):
#     """
#     Сериализует данные для добавления товаров в корзину.
#     Проверяет наличие корзины для юзера и добавляет товар.
#     """

#     def save(self, **kwargs):
#         product = Product.objects.filter(
#             slug=self.context['product_slug']).first()
#         user = self.context['user']
#         shop_basket = Shop_basket.objects.get_or_create(customer=user)
#         shop_basket_item = Shop_basket_items.objects.get_or_create(
#             shop_basket=shop_basket[0], product=product
#         )
#         if 'quantity' in self.validated_data:
#             quantity = self.validated_data['quantity']
#             if quantity == 0:
#                 quantity = 1
#             shop_basket_item[0].quantity += quantity
#         else:
#             shop_basket_item[0].quantity += 1
#         shop_basket_item[0].save()
#         self.instance = shop_basket_item[0]

#         return self.instance

#     def validate(self, value):
#         product = Product.objects.filter(
#             slug=self.context['product_slug']).first()
#         if "quantity" in value:
#             if value['quantity'] <= 0:
#                 raise serializers.ValidationError(
#                     'Количество товара должно быть больше 0')
#             if value['quantity'] > product.quantity:
#                 raise serializers.ValidationError(
#                     'Количество товара больше, чем в наличии на складе.')
#         return value

#     class Meta:
#         model = Shop_basket_items
#         fields = ('id', 'quantity',)
