from django.shortcuts import render
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["GET"])
def product_list(request):
    products = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def product_list_detail(request, product_id):
    product = get_object_or_404(DepositProducts, pk=product_id)
    serializer = DepositProductsSerializer(product)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def product_option_list(request):
    products = DepositOptions.objects.all()
    serializer = DepositOptionsSerializer(products, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def product_option_list_detail(request, product_id):
    product = get_object_or_404(DepositOptions, pk=product_id)
    serializer = DepositOptionsSerializer(product)
    return Response(serializer.data, status.HTTP_200_OK)