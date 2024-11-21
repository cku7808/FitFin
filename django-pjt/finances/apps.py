from django.apps import AppConfig

class FinancesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "finances"
    
    # 서버 시작 시 실행
    def ready(self):
        from .scheduler import start_scheduler, save_exchangerate
        import atexit
        # 서버 시작 시 스케줄러 샐행
        # save_exchangerate()  # 환율 db 먼저 초기화 진행
        start_scheduler()  # 매일 오전 11시 1분마다 당일 환율로 db 업데이트
        
        # 서버 종료 시 스케줄러 정리
        atexit.register(self.stop_scheduler)

    def stop_scheduler(self):
        from .scheduler import shutdown_scheduler
        shutdown_scheduler()
        
# Django 라이브 리로드 기능 -> 서버 실행 시 같은 프로세스 두 번 실행
# Django에서는 디버그환경에서 코드를 변경하게 되면 그에따라 즉각적으로 장고 서버에 반영되는데 이렇게 됨
# 프로세스를 2개 만들어 하나는 기본적인 기능을 담당하고 다른 하나는 코드 변경을 감지하여 적용하는 식으로 진행되었기에 가능한 것
# 만약 디버그 상태에서 즉각적인 변화를 반영하고 싶지 않다면 "python manage.py runserver --noreload" 옵션을 붙여 실행
# https://jheaon.tistory.com/281