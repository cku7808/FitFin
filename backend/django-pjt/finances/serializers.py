from rest_framework import serializers
from .models import Currency, TodayCurrency, DepositProducts, \
SavingProducts, DepositOption, SavingOption, \
LoanProducts, LoanOption, LoanTotal

# 환율
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class TodayCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodayCurrency
        fields = '__all__'

# 금융 상품 저장
class DepositProductsDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class SavingProductsDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'

class LoanProductsDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProducts
        fields = '__all__'

class LoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOption
        fields = '__all__'
        # read_only_fields = ('deposit_product',)

class LoanTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanTotal
        fields = '__all__'
        # read_only_fields = ('deposit_product',)


# 금융 상품
class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = ('id', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'mtrt_int')

class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ('deposit_product',)

class DepositProductsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'
        
    options = DepositOptionSerializer(many=True)

class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = ('id', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm')

class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields = ('saving_product',)
        
class SavingProductsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'
    
    options = SavingOptionSerializer(many=True)