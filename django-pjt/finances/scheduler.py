import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger


def say():
    print("Hello!", time.strftime('%H:%M:%S'))

# 특정 시간에 환율 db 생성
def scheduler_dbupdate(self):
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')  # 시간대 설정
    # trigger = CronTrigger(hour=17, minute=35)  # 시간 설정
    trigger = IntervalTrigger(seconds=1)  # 시간 설정
    scheduler.add_job(
        say,
        trigger=trigger,
        id='test',
        replace_existing=True)
    scheduler.start() #스케줄러 작업 실행
    # return JsonResponse({'message': '실행 완료!'})