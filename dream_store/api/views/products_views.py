from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from products.models import Products
from api.serializers.products_serializers import ProductsSerializer


@api_view(['GET'])
def products_list(request):
    """
    Позволяет получить список товаров.
    """

    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)
