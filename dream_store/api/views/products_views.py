from django_filters import rest_framework as django_filters
from rest_framework import generics, filters
from rest_framework.permissions import (
    SAFE_METHODS, IsAdminUser, AllowAny,) 

from products.models import (
    Product, Category, Brand, CountryProduct)
from api.serializers.products_serializers import (
    ProductSerializer, ProductDetailSerializer,
    CategorySerializer, CategoryDetailSerializer,
    BrandSerializer, CountryProductSerializer)
from api.filters.products_filters import (
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

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить конкретный товар по {slug}, обновить запись
    или удалить ее полностью.
    """

    queryset = Product.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductDetailSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


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

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить конкретную категорию по {slug}, обновить запись
    или удалить ее полностью.
    """

    queryset = Category.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CategoryDetailSerializer
        return CategorySerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


class BrandList(generics.ListCreateAPIView):
    """
    Позволяет получить список брендов, либо добавить бренд.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить конкретную запись по {slug}, обновить запись
    или удалить ее полностью.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


class CountryProductList(generics.ListCreateAPIView):
    """
    Позволяет получить список брендов, либо добавить бренд.
    """

    queryset = CountryProduct.objects.all()
    serializer_class = CountryProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]


class CountryProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить конкретную запись по {pk}, обновить запись
    или удалить ее полностью.
    """

    queryset = CountryProduct.objects.all()
    serializer_class = CountryProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]
