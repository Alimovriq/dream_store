# from django.http import HttpResponse, JsonResponse
from django_filters import rest_framework as django_filters
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics, filters

from products.models import Product, Category
from api.serializers.products_serializers import (
    ProductSerializer, ProductDetailSerializer,
    CategorySerializer, CategoryDetailSerializer)
from api.filters.prdoucts_filters import ProductFilter


class ProductList(generics.ListCreateAPIView):
    """
    Позволяет получить список товаров, либо создать товар
    Фильтрация полей: максимальная и мининимальная стоимость;
    название категории; название бренда; название страны
    Поиск по названию товара (начиная с ).
    Сортировка по названию и цене товаров
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
    Позволяет получить список категорий, либо создать категорию
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # filter_backends = (
    #     django_filters.DjangoFilterBackend,
    #     filters.SearchFilter, filters.OrderingFilter,)
    # filterset_class = ProductFilter
    # search_fields = ('^name',)
    # ordering_fields = ('name', 'price', 'quantity')
    # ordering = ('name',)


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
