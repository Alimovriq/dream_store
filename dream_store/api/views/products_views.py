# from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from products.models import Products, Categories
from api.serializers.products_serializers import (
    ProductsSerializer, ProductsDetailSerializer,
    CategoriesSerializer,)


@api_view(['GET', 'POST'])
def products_list(request):
    """
    Позволяет получить список товаров и создать один экземпляр.
    """

    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data_parsed = JSONParser().parse(request)
        serializer = ProductsSerializer(data=data_parsed)
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
        product = Products.objects.get(slug=slug)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductsDetailSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data_parsed = JSONParser().parse(request)
        serializer = ProductsSerializer(product, data=data_parsed)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        data_parsed = JSONParser().parse(request)
        serializer = ProductsSerializer(product, data=data_parsed)
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

    if request.method == 'GET':
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(
            categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data_parsed = JSONParser().parse(request)
        serializer = CategoriesSerializer(data=data_parsed)
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
        category = Categories.objects.get(slug=slug)
    except Categories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategoriesSerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data_parsed = JSONParser().parse(request)
        serializer = CategoriesSerializer(category, data=data_parsed)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        data_parsed = JSONParser().parse(request)
        serializer = CategoriesSerializer(category, data=data_parsed)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
