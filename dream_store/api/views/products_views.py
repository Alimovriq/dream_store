# from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from products.models import Product, Category
from api.serializers.products_serializers import (
    ProductSerializer, ProductDetailSerializer,
    CategorySerializer, CategoryDetailSerializer)


@api_view(['GET', 'POST'])
def products_list(request):
    """
    Позволяет получить список товаров и создать один экземпляр.
    """

    paginator = PageNumberPagination()

    if request.method == 'GET':
        products = Product.objects.all()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        data_parsed = JSONParser().parse(request)
        serializer = ProductSerializer(data=data_parsed)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def products_detail(request, slug):
    """
    Позволяет получить конкретную запись, перезаписать, изменить, удалить.
    """

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data_parsed = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data_parsed)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        data_parsed = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data_parsed)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def categories_list(request):
    """
    Позволяет получить список категорий и создать один экземпляр.
    """

    paginator = PageNumberPagination()

    if request.method == 'GET':
        categories = Category.objects.all()
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategoryDetailSerializer(
            result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        data_parsed = JSONParser().parse(request)
        serializer = CategorySerializer(data=data_parsed)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def categories_detail(request, slug):
    """
    Позволяет получить конкретную запись, перезаписать, изменить, удалить.
    """

    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data_parsed = JSONParser().parse(request)
        serializer = CategorySerializer(category, data=data_parsed)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        data_parsed = JSONParser().parse(request)
        serializer = CategorySerializer(category, data=data_parsed)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
