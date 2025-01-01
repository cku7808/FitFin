import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta, timezone
import requests

import os

from airflow.models import Variable

FINANCE_API_KEY = Variable.get("api_key_financial")
CURRENCY_API_KEY = Variable.get("api_key_currency")

def get_deposit_products_api():
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': FINANCE_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()

        # Django API에 데이터 전달
        django_response = requests.post(
            "https://django-backend-service-579042790724.asia-northeast1.run.app/api/v2/save-deposit-products/",
            json=data
        )
        # if django_response.status_code != 201:
        #     raise Exception(f"Failed to save data: {django_response.json()}")
    else:
        raise Exception("Failed to deposit data from API")
    
def get_saving_products_api():
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
    URL = BASE_URL + 'savingProductsSearch.json'
    params = {
        'auth': FINANCE_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()

        # Django API에 데이터 전달
        django_response = requests.post(
            "https://django-backend-service-579042790724.asia-northeast1.run.app/api/v2/save-saving-products/",
            json=data
        )
        # if django_response.status_code != 201:
        #     raise Exception(f"Failed to save data: {django_response.json()}")
    else:
        raise Exception("Failed to saving data from API")

def get_loan_products_api():
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
    URL = BASE_URL + 'creditLoanProductsSearch.json'
    params = {
        'auth': FINANCE_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()
        
        # Django API에 데이터 전달
        django_response = requests.post(
            "https://django-backend-service-579042790724.asia-northeast1.run.app/api/v2/save-laon-products/",
            json=data
        )
        # if django_response.status_code != 201:
        #     raise Exception(f"Failed to save data: {django_response.json()}")
    else:
        raise Exception("Failed to loan data from API")

def get_loan_total_api():
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
    URL = BASE_URL + 'creditLoanProductsSearch.json'
    params = {
        'auth': FINANCE_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()

        # Django API에 데이터 전달
        django_response = requests.post(
            "https://django-backend-service-579042790724.asia-northeast1.run.app/api/v2/save-laon-total/",
            json=data
        )
        # if django_response.status_code != 201:
        #     raise Exception(f"Failed to save data: {django_response.json()}")
    else:
        raise Exception("Failed to loan total data from API")

# def save_exchangerate():
#     url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={CURRENCY_API_KEY}&seaerchdate=241122&data=AP01'
#     response = requests.get(url, verify=False)

#     if response.status_code == 200:
#         data = response.json()

#         # Django API에 데이터 전달
#         django_response = requests.post(
#             "https://django-backend-service-579042790724.asia-northeast1.run.app/api/v2/save-laon-total/",
#             json=data
#         )
#         # if django_response.status_code != 201:
#         #     raise Exception(f"Failed to save data: {django_response.json()}")
#     else:
#         raise Exception("Failed to loan total data from API")

# * * * * *
# - - - - -
# | | | | |
# | | | | └─ 요일 (0-6, 0=일요일, 1=월요일, ..., 6=토요일)
# | | | └── 월 (1-12)
# | | └─── 일 (1-31)
# | └──── 시 (0-23)
# └───── 분 (0-59)

KST = timezone(timedelta(hours=9))

# with DAG(
# 	dag_id = "exchange_dag", # 원하는 DAG 이름 지정 
# 	start_date = datetime(2024, 12, 23, tzinfo=KST), # DAG 처음 실행 시작 날짜
# 	schedule_interval = "10 11 * * 1-5" # 주중 11시 10분
# ) as exchange_dag:
#     updateall_exchangerate = PythonOperator( 
#         task_id = "updateall_exchangerate", 
#         python_callable = updateall_exchangerate, 						
#         dag = exchange_dag 
#     )

with DAG(
	dag_id = "product_dag", # 원하는 DAG 이름 지정 
	start_date = datetime(2024, 12, 23, tzinfo=KST), # DAG 처음 실행 시작 날짜
	schedule_interval="0 10 * * 1", # 매주 월요일 10시
) as product_dag :
    get_deposit_products_api = PythonOperator( 
        task_id = "get_deposit_products_api", 
        python_callable = get_deposit_products_api, 											
    )

    get_saving_products_api = PythonOperator(
        task_id = "get_saving_products_api", 
        python_callable = get_saving_products_api, 			
    )

    get_loan_products_api = PythonOperator( 
        task_id = "get_loan_products_api", 
        python_callable = get_loan_products_api,							
    )

    get_loan_total_api = PythonOperator( 
        task_id = "get_loan_total_api", 
        python_callable = get_loan_total_api,									
    )
