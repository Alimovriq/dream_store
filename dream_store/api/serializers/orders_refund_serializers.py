from rest_framework import serializers

from orders.models import OrderRefund, OrderItemsRefund


class OrderRefundSerializerCreate(serializers.ModelSerializer):
    """
    Сериализатор при создании возврата для товаров.
    """

    class Meta:
        model = OrderRefund
        fields = (
            'order',
            'comment',
        )


class OrderItemsRefundSerializerCreate(serializers.ModelSerializer):
    """
    Сериализатор при создании товаров для возврата.
    """

    refund = OrderRefundSerializerCreate()
    order_item = serializers.CharField(source='order_item.product.name')

    class Meta:
        model = OrderItemsRefund
        fields = (
            'refund',
            'order_item',
            'quantity',
        )

    def create(self, validated_data):
        order_obj = validated_data.pop('refund')['order']
        order_refund = OrderRefund.objects.get_or_create(order=order_obj)
        for item in validated_data:
            obj = OrderItemsRefund.objects.create(refund=order_refund, **item)
        return obj


class OrderItemsRefundSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения товаров, которые для возврата.
    """

    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    vendor_code = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    refund_amount = serializers.SerializerMethodField()

    class Meta:
        model = OrderItemsRefund
        fields = (
            'id',
            'name',
            'brand',
            'category',
            'image',
            'country',
            'vendor_code',
            'slug',
            'price',
            'quantity',
            'refund_amount',
        )

    def get_name(self, obj):
        return obj.order_item.product.name

    def get_price(self, obj):
        return obj.order_item.product.price

    def get_brand(self, obj):
        return obj.order_item.product.brand.name

    def get_category(self, obj):
        return obj.order_item.product.category.name

    def get_image(self, obj):
        url = self.context.get_host()
        im = obj.order_item.product.image
        return url + im if im else 'null'

    def get_country(self, obj):
        return obj.order_item.product.country.name

    def get_vendor_code(self, obj):
        return obj.order_item.product.vendor_code

    def get_slug(self, obj):
        return obj.order_item.product.slug

    def get_refund_amount(self, obj):
        return obj.order_item.product.price * obj.quantity


class OrderRefundSerializer(serializers.ModelSerializer):
    """
    Сериализатор для главной модели возвратов.
    """

    refund_items = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderRefund
        fields = (
            'id',
            'order',
            'refund_items',
            'created_at',
            'comment',
            'status',
        )

    # def create(self, validated_data):
    #     refund_items_data = validated_data.pop('refund_items')
    #     order_refund = OrderRefund.objects.create(**validated_data)
    #     for item_data in refund_items_data:
    #         OrderItemsRefund.objects.create(refund=order_refund, **item_data)
    #     return order_refund

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     refund_items = OrderItemsRefund.objects.filter(refund=instance)
    #     ret['refund_items'] = OrderItemsRefundSerializer(
    #         refund_items, many=True).data
    #     return ret

    def get_refund_items(self, obj):
        context = self.context.get('request')
        order_refund_items = OrderItemsRefund.objects.filter(refund=obj)
        return OrderItemsRefundSerializer(
            order_refund_items, many=True, context=context).data
