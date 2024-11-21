from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.conf import settings
import requests
from datetime import datetime, timedelta

from .models import Currency, DepositProducts, DepositOption, SavingProducts, SavingOption
from .serializers import CurrencySerializer, DepositProductsSerializer, SavingProductsSerializer, DepositOptionSerializer, SavingOptionSerializer

# X환율 계산X (테스트 용)
@api_view(['GET'])
def save_exchangerate(request):
    api_key = settings.API_KEY['currency']
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&data=AP01'
    response = requests.get(url, verify=False).json()
    
#     if not response:
#         yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
#         url = url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate={yesterday}&data=AP01'
#         response = requests.get(url, verify=False).json()
#         print('오늘자 환율 업데이트 전!')
    
    # Currency.objects.all().delete()  # 초기화

    # for li in response:  # 환율 정보 저장
    #     cur_unit = li.get('cur_unit').replace('(100)', '')
    #     cur_nm = li.get('cur_nm').replace('유로', '유럽연합 유로').replace('위안화', '중국 위안화')
    #     ttb = li.get('ttb')
    #     tts = li.get('tts')
    #     deal_bas_r = li.get('deal_bas_r')
    #     bkpr = li.get('bkpr')
    #     yy_efee_r = li.get('yy_efee_r')
    #     ten_dd_efee_r = li.get('ten_dd_efee_r')
    #     kftc_deal_bas_r = li.get('kftc_deal_bas_r')
    #     kftc_bkpr = li.get('kftc_bkpr')

    #     if (cur_unit == 'JPY') or (cur_unit == 'IDR'):
    #         ttb = float(ttb)/100
    #         tts = float(tts)/100
    #         deal_bas_r = float(deal_bas_r)/100
    #         bkpr = float(bkpr)/100
    #         yy_efee_r = float(yy_efee_r)/100
    #         ten_dd_efee_r = float(ten_dd_efee_r)/100
    #         kftc_deal_bas_r = float(kftc_deal_bas_r)/100
    #         kftc_bkpr = float(kftc_bkpr)/100

    #     save_data = {
    #         'cur_unit': cur_unit,
    #         'cur_nm': cur_nm.split()[1],
    #         'cur_con': cur_nm.split()[0],
    #         'ttb': ttb,
    #         'tts': tts,
    #         'deal_bas_r': deal_bas_r,
    #         'bkpr': bkpr,
    #         'yy_efee_r': yy_efee_r,
    #         'ten_dd_efee_r': ten_dd_efee_r,
    #         'kftc_deal_bas_r': kftc_deal_bas_r,
    #         'kftc_bkpr': kftc_bkpr,
    #     } 
    
    #     # print(cur_nm.split()[0], ':', ttb)

    #     serializer = CurrencySerializer(data=save_data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    
    return JsonResponse({'message': '저장 성공!'})
    # return Response(response)

# 당일 환율 정보 로드
@api_view(['GET'])
def load_exchagerate(request):
    date = datetime.now().strftime('%Y%m%d')
    if not Currency.objects.filter(date=date).exists():
        date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    print(date)
    currencies = Currency.objects.filter(date=date)
    serializers = CurrencySerializer(currencies, many=True)
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

    
