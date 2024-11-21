from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta

from django.conf import settings
import requests
from .models import Currency, TodayCurrency
from .serializers import CurrencySerializer, TodayCurrencySerializer

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

scheduler = BackgroundScheduler(timezone='Asia/Seoul')  # 시간대 설정

# 스케줄러 테스트 함수
def test_scheduler():
    # 현재 시간으로 되어있긴한데 django settings.py seoul로 바꿔야될수도
    print("Hello!", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  

# 오늘 환율 정보 업데이트 (db, 그래프)
def updatetoday_exchangerate():
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

# 환율 db 저장 (초기 세팅)
def save_exchangerate():
    api_key = settings.API_KEY['currency']
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&data=AP01'
    response = requests.get(url, verify=False).json()

    today = datetime.now()
    if not response:  # 오늘 환율 아직 업데이트 전이면
        print('오늘자 환율 업데이트 전!')
        today = datetime.now() - timedelta(days=1)
    
    Currency.objects.all().delete()  # 초기화

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
    
    # 환율 당일 정보 업데이트
    updatetoday_exchangerate()

    print('전체 환율 db 업데이트!!!')
    
# 환율 전체 db 업데이트 (당일 환율 갱신됐다고 가정)
def updateall_exchangerate():
    date_now = datetime.now().strftime('%Y%m%d')
    date_past = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    Currency.objects.filter(date=date_past).delete()  # 7일 전 데이터 삭제
    
    api_key = settings.API_KEY['currency']
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&data=AP01'
    response = requests.get(url, verify=False).json()
    
    for li in response:  # 오늘의 환율 정보 저장
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
                'date': date_now,
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

    # 환율 당일 정보 업데이트
    updatetoday_exchangerate()

    print('오늘 환율 db 업데이트!!!')

# 특정 시간에 환율 db 업데이트
def start_scheduler():
    if not scheduler.running:
        trigger = CronTrigger(hour=11, minute=1)  # 시간 설정
        # trigger = IntervalTrigger(seconds=2)  # 시간 설정
        scheduler.add_job(
            updateall_exchangerate,
            # test_scheduler,
            trigger=trigger,
            id='test',
            replace_existing=True)
        scheduler.start() #스케줄러 작업 실행
        # return JsonResponse({'message': '실행 완료!'})
    
# 스케줄러 정리
def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)  # 스케줄러 종료
        print("Scheduler stopped.")
