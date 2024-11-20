from django.apps import AppConfig
from django.core.signals import request_finished


class FinancesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "finances"


# 서버 시작 시 실행
class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'finances'

    def ready(self):
        # 서버 시작 시 스케줄러 샐행
        from .scheduler import scheduler_dbupdate   
        scheduler_dbupdate()


        # 서버 종료 시 스케줄러 정리
        # def shutdown_scheduler(sender, **kwargs):
        #     print('Shutting down scheduler')
        #     BackgroundScheduler.shutdown()
        # request_finished.connect(shutdown_scheduler)