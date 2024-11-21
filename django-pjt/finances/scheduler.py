from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta

from django.conf import settings
import requests
from .models import Currency
from .serializers import CurrencySerializer

scheduler = BackgroundScheduler(timezone='Asia/Seoul')  # 시간대 설정

# 스케줄러 테스트 함수
def test_scheduler():
    # 현재 시간으로 되어있긴한데 django settings.py seoul로 바꿔야될수도
    print("Hello!", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  
    
# 환율 db 저장
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
            ttb = li.get('ttb')
            tts = li.get('tts')
            deal_bas_r = li.get('deal_bas_r')
            bkpr = li.get('bkpr')
            yy_efee_r = li.get('yy_efee_r')
            ten_dd_efee_r = li.get('ten_dd_efee_r')
            kftc_deal_bas_r = li.get('kftc_deal_bas_r')
            kftc_bkpr = li.get('kftc_bkpr')

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

    print('전체 환율 db 업데이트!!!')
    
# 환율 db 업데이트 (당일 환율 갱신됐다고 가정)
def update_exchangerate():
    date_now = datetime.now().strftime('%Y%m%d')
    date_past = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    Currency.objects.filter(date=date_past).delete()  # 7일 전 데이터 삭제
    
    api_key = settings.API_KEY['currency']
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&data=AP01'
    response = requests.get(url, verify=False).json()
    
    for li in response:  # 오늘의 환율 정보 저장
            cur_nm = li.get('cur_nm').replace('유로', '유럽연합 유로').replace('위안화', '중국 위안화')
            cur_unit = li.get('cur_unit').replace('(100)', '')
            ttb = li.get('ttb')
            tts = li.get('tts')
            deal_bas_r = li.get('deal_bas_r')
            bkpr = li.get('bkpr')
            yy_efee_r = li.get('yy_efee_r')
            ten_dd_efee_r = li.get('ten_dd_efee_r')
            kftc_deal_bas_r = li.get('kftc_deal_bas_r')
            kftc_bkpr = li.get('kftc_bkpr')

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

    print('오늘 환율 db 업데이트!!!')
    
# 특정 시간에 환율 db 업데이트
def start_scheduler():
    if not scheduler.running:
        trigger = CronTrigger(hour=11, minute=1)  # 시간 설정
        # trigger = IntervalTrigger(seconds=2)  # 시간 설정
        scheduler.add_job(
            update_exchangerate,
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
