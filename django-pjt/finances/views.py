from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
import requests

from django.conf import settings

from .models import Currency, DepositProducts, DepositOption, SavingProducts, SavingOption
from .serializers import CurrencySerializer, DepositProductsSerializer, SavingProductsSerializer, DepositOptionSerializer, SavingOptionSerializer


# 환율 계산
@api_view(['GET'])
def exchangerate(request):
    api_key = settings.API_KEY['currency']
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&data=AP01'
    response = requests.get(url, verify=False).json()
    serializers = CurrencySerializer(data=response, many=True)
    if serializers.is_valid(raise_exception=True):
        serializers.save()

    # 스케줄러로 매일 11시마다 db에 환율 저장
    
    return Response(serializers.data)


# 금융상품정보
    # 페이지 하나만 가져옴 (페이지 1번 밖에 존재 안 함?)
@api_view(['GET'])
def save_deposit_products(request):  # 예금 상품
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': settings.API_KEY['financial'],
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }

    response = requests.get(URL, params=params).json()
    test_nm = 0

    for li in response.get('result').get('baseList'):  # 예금 상품 정보 저장
        dcls_month = li.get('dcls_month')
        fin_co_no = li.get('fin_co_no')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_cd = li.get('fin_prdt_cd')
        fin_prdt_nm = li.get('fin_prdt_nm')
        join_way = li.get('join_way')
        mtrt_int = li.get('mtrt_int')
        spcl_cnd = li.get('spcl_cnd')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        etc_note = li.get('etc_note')
        max_limit = li.get('max_limit')
        dcls_strt_day = li.get('dcls_strt_day')
        dcls_end_day = li.get('dcls_end_day')
        
        if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        save_data = {
            'dcls_month': dcls_month,
            'fin_co_no': fin_co_no,
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': kor_co_nm,
            'fin_prdt_nm': fin_prdt_nm,
            'join_way': join_way,
            'mtrt_int': mtrt_int,
            'spcl_cnd': spcl_cnd,
            'join_deny': join_deny,
            'join_member': join_member,
            'etc_note': etc_note,
            'max_limit': max_limit,
            'dcls_strt_day': dcls_strt_day,
            'dcls_end_day': dcls_end_day,
        }

        serializer = DepositProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for li in response.get('result').get('optionList'):  # 예금 옵션 정보 저장
        dcls_month = li.get('dcls_month')
        fin_co_no = li.get('fin_co_no')
        fin_prdt_cd = li.get('fin_prdt_cd')  # 예금 상품명
        intr_rate_type = li.get('intr_rate_type')  # 유형 or 유형명 중에 하나만 저장해도 될듯?
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        intr_rate = li.get('intr_rate2')
        intr_rate2 = li.get('intr_rate2')
        save_trm = li.get('save_trm')

        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
              
        if DepositOption.objects.filter(deposit_product=product, intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2, save_trm=save_trm).exists():
            continue

        save_data = {
            'dcls_month': dcls_month,
            'fin_co_no': fin_co_no,
            # 'fin_prdt_cd': fin_prdt_cd,  # 외래 키 설정 (deposit_product)
            'intr_rate_type': intr_rate_type,
            'intr_rate_type_nm': intr_rate_type_nm,
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
            'save_trm': save_trm,
        }

        serializer = DepositOptionSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(deposit_product=product)
            
    return JsonResponse({'message': '저장 성공!'})


@api_view(['GET'])
def save_saving_products(request):  # 적금 상품
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
    URL = BASE_URL + 'savingProductsSearch.json'
    params = {
        'auth': settings.API_KEY['financial'],
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }

    response = requests.get(URL, params=params).json()

    for li in response.get('result').get('baseList'):  # 적금 상품 정보 저장
        dcls_month = li.get('dcls_month')
        fin_co_no = li.get('fin_co_no')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_cd = li.get('fin_prdt_cd')
        fin_prdt_nm = li.get('fin_prdt_nm')
        join_way = li.get('join_way')
        mtrt_int = li.get('mtrt_int')
        spcl_cnd = li.get('spcl_cnd')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        etc_note = li.get('etc_note')
        max_limit = li.get('max_limit')
        dcls_strt_day = li.get('dcls_strt_day')
        dcls_end_day = li.get('dcls_end_day')
        
        
        if SavingProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        save_data = {
            'dcls_month': dcls_month,
            'fin_co_no': fin_co_no,
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': kor_co_nm,
            'fin_prdt_nm': fin_prdt_nm,
            'join_way': join_way,
            'mtrt_int': mtrt_int,
            'spcl_cnd': spcl_cnd,
            'join_deny': join_deny,
            'join_member': join_member,
            'etc_note': etc_note,
            'max_limit': max_limit,
            'dcls_strt_day': dcls_strt_day,
            'dcls_end_day': dcls_end_day,
        }

        serializer = SavingProductsSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for li in response.get('result').get('optionList'):  # 예금 옵션 정보 저장
        dcls_month = li.get('dcls_month')
        fin_co_no = li.get('fin_co_no')
        fin_prdt_cd = li.get('fin_prdt_cd')  # 예금 상품명
        intr_rate_type = li.get('intr_rate_type')  # 유형 or 유형명 중에 하나만 저장해도 될듯?
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        intr_rate = li.get('intr_rate2')
        intr_rate2 = li.get('intr_rate2')
        rsrv_type = li.get('rsrv_type')
        rsrv_type_nm = li.get('rsrv_type_nm')  # 유형 or 유형명 중에 하나만 저장해도 될듯?
        save_trm = li.get('save_trm')

        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
              
        if SavingOption.objects.filter(saving_product=product, intr_rate_type_nm=intr_rate_type_nm, intr_rate=intr_rate, intr_rate2=intr_rate2, save_trm=save_trm, rsrv_type_nm=rsrv_type_nm).exists():
            continue

        save_data = {
            'dcls_month': dcls_month,
            'fin_co_no': fin_co_no,
            # 'fin_prdt_cd': fin_prdt_cd,
            'intr_rate_type': intr_rate_type,
            'intr_rate_type_nm': intr_rate_type_nm,
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
            'rsrv_type': rsrv_type,
            'rsrv_type_nm': rsrv_type_nm,
            'save_trm': save_trm,
        }

        serializer = SavingOptionSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(saving_product=product)

    return JsonResponse({'message': '저장 성공!'})

    
