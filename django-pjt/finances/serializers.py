from rest_framework import serializers
from .models import Currency, TodayCurrency, DepositProducts, SavingProducts, DepositOption, SavingOption

# 환율
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class TodayCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodayCurrency
        fields = '__all__'


# 금융 상품
class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ('deposit_product',)

class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'

class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields = ('saving_product',)
