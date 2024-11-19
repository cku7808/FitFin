from rest_framework import serializers
from .models import DepositOptions, DepositProducts

class DepositProductsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = ('fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm')
        
class DepositProductsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = "__all__"

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = "__all__"
        read_only_fields = ("product",)
