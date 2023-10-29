from django_filters import rest_framework as filters

# import django_filters

from products.models import Product


class ProductFilter(filters.FilterSet):
    """
    Фильтрация для товаров.
    """

    min_price = filters.NumberFilter(field_name='price',
                                     lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price',
                                     lookup_expr='lte')
    category = filters.CharFilter(field_name='category__name',
                                  lookup_expr='icontains')
    brand = filters.CharFilter(field_name='brand__name',
                               lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('brand',
                  'name',
                  'category',
                  'country')
