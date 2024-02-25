from django_filters import rest_framework as filters

from products.models import Product, Category


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
    country = filters.CharFilter(field_name='country__name',
                                 lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('brand',
                  'name',
                  'category',
                  'country')


class CategoryFilter(filters.FilterSet):
    """
    Фильтрация для категорий.
    """

    class Meta:
        model = Category
        fields = ('name',)
