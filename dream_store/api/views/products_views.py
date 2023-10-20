from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from products.models import Products
from api.serializers.products_serializers import ProductsSerializer


@api_view(['GET', 'POST'])
def products_list(request):
    """
    Позволяет получить список товаров и создать один экземпляр.
    """

    if request.method == 'GET':
        # Надо при запросе в поле Category возвращать все строки экземпляра.
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
