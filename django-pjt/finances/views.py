from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.conf import settings
import requests
from datetime import datetime, timedelta

from .models import Currency, TodayCurrency, DepositProducts, DepositOption, SavingProducts, SavingOption
from .serializers import CurrencySerializer, TodayCurrencySerializer, DepositProductsSerializer, SavingProductsSerializer, DepositOptionSerializer, SavingOptionSerializer

# 그래프 그리기
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


# <<<<<테스트 용 함수>>>>>>>>
# 환율 계산
@api_view(['GET'])
def save_exchangerate(request):
    api_key = settings.API_KEY['currency']
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&data=AP01'
    response = requests.get(url, verify=False).json()

    today = datetime.now()
    if not response:  # 오늘 환율 아직 업데이트 전이면
        print('오늘자 환율 업데이트 전!')
        today = datetime.now() - timedelta(days=1)
    
    Currency.objects.all().delete()  # 초기화
    TodayCurrency.objects.all().delete()  # 초기화

    # 일주일 정보 저장
    for day in reversed(range(7)):
        date = (today - timedelta(days=day)).strftime('%Y%m%d')
        url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate={date}&data=AP01'
        response = requests.get(url, verify=False).json()

        for li in response:  # 환율 정보 저장
            cur_nm = li.get('cur_nm').replace('유로', '유럽연합 유로').replace('위안화', '중국 위안화')
            cur_unit = li.get('cur_unit').replace('(100)', '')
            ttb = li.get('ttb').replace(',', '')
            tts = li.get('tts').replace(',', '')
            deal_bas_r = li.get('deal_bas_r').replace(',', '')
            bkpr = li.get('bkpr').replace(',', '')
            yy_efee_r = li.get('yy_efee_r').replace(',', '')
            ten_dd_efee_r = li.get('ten_dd_efee_r').replace(',', '')
            kftc_deal_bas_r = li.get('kftc_deal_bas_r').replace(',', '')
            kftc_bkpr = li.get('kftc_bkpr').replace(',', '')

            if (cur_unit == 'JPY') or (cur_unit == 'IDR'):
                ttb = float(ttb)/100
                tts = float(tts)/100
                deal_bas_r = float(deal_bas_r)/100
                bkpr = float(bkpr)/100
                yy_efee_r = float(yy_efee_r)/100
                ten_dd_efee_r = float(ten_dd_efee_r)/100
                kftc_deal_bas_r = float(kftc_deal_bas_r)/100
                kftc_bkpr = float(kftc_bkpr)/100

            save_data = {
                'date': date,
                'cur_con': cur_nm.split()[0],
                'cur_nm': cur_nm.split()[1],
                'cur_unit': cur_unit,
                'ttb': ttb,
                'tts': tts,
                'deal_bas_r': deal_bas_r,
                'bkpr': bkpr,
                'yy_efee_r': yy_efee_r,
                'ten_dd_efee_r': ten_dd_efee_r,
                'kftc_deal_bas_r': kftc_deal_bas_r,
                'kftc_bkpr': kftc_bkpr,
            } 
        
            serializer = CurrencySerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            # 오늘 환율 정보 backbone 세팅
            if day == 0:

                if (cur_unit == 'JPY') or (cur_unit == 'IDR'):
                    cur_unit += ' 100'
                    cur_nm += ' 100'
                    deal_bas_r *= 100
                
                save_data = {
                'cur_con': cur_nm.split()[0],
                'cur_nm': cur_nm.split()[1],
                'cur_unit': cur_unit,
                'deal_bas_r': deal_bas_r,
                'img': f'/static/finances/{cur_nm.split()[0]}.png',
                # 'yesterday_diff': yesterday_diff,
                # 'yesterday_per': yesterday_per,
                }
                
                serializer = TodayCurrencySerializer(data=save_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

    print('전체 환율 db 업데이트!!!')
    
    return JsonResponse({'message': '저장 성공!'})
    # return Response(response)

# 오늘 환율 정보 업데이트 (차이, 퍼센트, 그래프용)
@api_view(['GET'])
def updatetoday_exchangerate(request):
    # 날짜 설정 (업데이트 전후로 오늘 날짜를 오늘 또는 어제로 설정)
    today = datetime.now()
    if not Currency.objects.filter(date=today.strftime('%Y%m%d')).exists():
        today = datetime.now() - timedelta(days=1)
        print('오늘자 환율 업데이트 전!')

    date_now = today.strftime('%Y%m%d')
    date_yes = (today - timedelta(days=1)).strftime('%Y%m%d')

    # 오늘 환율 정보 db 업데이트
    currenecies = TodayCurrency.objects.all()
    for currency_today in currenecies:
        # 오늘 환율 정보 db 업데이트
        currency_now = Currency.objects.get(date=date_now, cur_con=currency_today.cur_con)
        currency_yes = Currency.objects.get(date=date_yes, cur_con=currency_today.cur_con)
        
        now_deal_bas_r = float(currency_now.deal_bas_r)
        yesterday_diff = float(currency_now.deal_bas_r) - float(currency_yes.deal_bas_r)
        yesterday_per = round((float(currency_now.deal_bas_r) - float(currency_yes.deal_bas_r)) / float(currency_yes.deal_bas_r) * 100, 2)
        
        if (currency_today.cur_unit == 'JPY 100') or (currency_today.cur_unit == 'IDR'):
            now_deal_bas_r = now_deal_bas_r * 100
            yesterday_diff = yesterday_diff * 100
        
        yesterday_diff = round(yesterday_diff, 2)


        # 변동 값에 따라 기호 설정 (색상 변경 때문에 front에서 하는게 나을 수도)
        if yesterday_diff > 0:
            yesterday_diff = '▲ ' + str(abs(yesterday_diff))
        elif yesterday_diff < 0:
            yesterday_diff = '▼ ' + str(abs(yesterday_diff))
        else:
            yesterday_diff = '0'

        currency_today.deal_bas_r = now_deal_bas_r
        currency_today.yesterday_diff = yesterday_diff
        currency_today.yesterday_per = yesterday_per
        

        
        currency_today.save()

        # 그래프 그리기 및 저장
        # 데이터 로드
        currencies_pre = Currency.objects.filter(cur_con=currency_today.cur_con).order_by('date')
        currency_dates = [currency_pre.date for currency_pre in currencies_pre]
        currency_rates = [float(currency_pre.deal_bas_r) for currency_pre in currencies_pre]

        path_graph = f'{settings.BASE_DIR}/finances/static/finances/{currency_today.cur_con}.png'  # 경로 설정
        
        # 사용자 정의 그라데이션 컬러맵 생성
        colors = ["#F3FDF6", "#79F297"]  # 밝은 색 -> 어두운 색
        cmap = LinearSegmentedColormap.from_list("custom_gradient", colors)
        fig, ax = plt.subplots(figsize=(4,2), facecolor="white")
        ax.plot(currency_dates, currency_rates, color = '#60BF78')

        #create the gradient fill
        #create the gradient image in the background
        ax.imshow(np.linspace(0, 1, 256).reshape(-1, 1),          #gradient array
                cmap=cmap,                                    #gradient color
                vmin=0.28,                                      #start of the gradient color
                aspect='auto',
                alpha = 0.9,                                    #transparency
                    extent=[currency_dates[0],                                   #start of x axis
                            currency_dates[-1],    #end of x axis - convert the datetime index to matplotlib dates
                            min(currency_rates)*0.99,                                   #start of y axis
                            max(currency_rates)],                  #end of y axis
                            origin='lower')                     #gradient orientation
        #color white the upper part of the chart
        ax.fill_between(currency_dates,                                #x axis values
                        currency_rates,                              #to y axis values
                        max(currency_rates),                        #y axis to y max
                        color = 'white')                          #color white between y value and y max
        # 축 없애기
        ax.axis("off")
        # 저장
        plt.savefig(path_graph, bbox_inches='tight')
        
        plt.cla()   # clear the current axes
        plt.clf()   # clear the current figure 
        plt.close() # closes the current figure

    return JsonResponse({'message': '저장 성공!'})

# <<<<<테스트 용 함수>>>>>>>>


# 당일 환율 정보 로드 (new)
@api_view(['GET'])
def load_today_exchangerate(request):
    currencies = TodayCurrency.objects.all()
    serializers = TodayCurrencySerializer(currencies, many=True)
    return Response(serializers.data)

# 당일 환율 정보 로드
@api_view(['GET'])
def load_exchangerate(request):
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

    
