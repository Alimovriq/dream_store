from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import status, generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from products.models import (
    Product, Category, Brand, CountryProduct)
from api.serializers.products_serializers import (
    ProductSerializer, ProductDetailSerializer,
    CategorySerializer, CategoryDetailSerializer,
    BrandSerializer, CountryProductSerializer)
from api.filters.prdoucts_filters import (
    ProductFilter, CategoryFilter)


class ProductList(generics.ListCreateAPIView):
    """
    Позволяет получить список товаров, либо создать товар.
    Фильтрация полей: максимальная и мининимальная стоимость;
    название категории; название бренда; название страны
    Поиск по названию товара (начиная с ).
    Сортировка по названию и цене товаров.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter,)
    filterset_class = ProductFilter
    search_fields = ('^name',)
    ordering_fields = ('name', 'price', 'quantity')
    ordering = ('name',)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить конкретный товар по {slug}, обновить запись
    или удалить ее полностью.
    """

    queryset = Product.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductDetailSerializer
        return ProductSerializer


class CategoryList(generics.ListCreateAPIView):
    """
    Позволяет получить список категорий, либо создать категорию.
    Фильтрация полей: название категории;
    Поиск по названию категории (начиная с ).
    Сортировка по названию категорий.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter,)
    filterset_class = CategoryFilter
    search_fields = ('^name',)
    ordering_fields = ('name',)
    ordering = ('name',)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить конкретную категорию по {slug}, обновить запись
    или удалить ее полностью.
    """

    queryset = Category.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryDetailSerializer
        return CategorySerializer


class BrandList(generics.ListCreateAPIView):
    """
    Позволяет получить список брендов, либо добавить бренд.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить конкретную запись по {slug}, обновить запись
    или удалить ее полностью.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'


class CountryProductList(generics.ListCreateAPIView):
    """
    Позволяет получить список брендов, либо добавить бренд.
    """

    queryset = CountryProduct.objects.all()
    serializer_class = CountryProductSerializer


class CountryProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить конкретную запись по {pk}, обновить запись
    или удалить ее полностью.
    """

    queryset = CountryProduct.objects.all()
    serializer_class = CountryProductSerializer
