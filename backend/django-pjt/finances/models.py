from django.db import models

# Create your models here.

# 환율 (일 데이터만 저장 - 매일 11시 업데이트)
class Currency(models.Model):
    date = models.CharField(max_length=100)             # 날짜
    cur_con = models.CharField(max_length=100)          # 국가
    cur_nm = models.CharField(max_length=100)           # 통화명
    cur_unit = models.CharField(max_length=100)         # 통화코드
    ttb = models.CharField(max_length=100)              # 전신환(송금) 받으실때
    tts = models.CharField(max_length=100)              # 전신환(송금) 보내실때
    deal_bas_r = models.CharField(max_length=100)       # 매매 기준율
    bkpr = models.CharField(max_length=100)             # 장부 가격
    yy_efee_r = models.CharField(max_length=100)        # 년환가료율
    ten_dd_efee_r = models.CharField(max_length=100)    # 10일환가료율
    kftc_deal_bas_r = models.CharField(max_length=100)  # 서울외국환중개 매매 기준율
    kftc_bkpr = models.CharField(max_length=100)        # 서울외국환중개 장부 가격

# 오늘의 환율
class TodayCurrency(models.Model):
    cur_con = models.CharField(max_length=100)          # 국가
    cur_nm = models.CharField(max_length=100)           # 통화명
    cur_unit = models.CharField(max_length=100)         # 통화코드
    deal_bas_r = models.CharField(max_length=100, null=True)       # 매매 기준율
    yesterday_diff = models.CharField(max_length=100, null=True)   # 증감 값
    yesterday_per = models.CharField(max_length=100, null=True)   # 증감 퍼센트
    img = models.CharField(max_length=100, null=True)   # 이미지 경로
     


# 금융 상품
class DepositProducts(models.Model):                            # 예금 상품
    dcls_month = models.CharField(max_length=20)                # 공시 제출월
    fin_co_no = models.CharField(max_length=100)                # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)                # 금융회사 명
    fin_prdt_cd = models.CharField(max_length=100)              # 금융상품 코드 
    fin_prdt_nm = models.CharField(max_length=100)              # 금융상품 명
    join_way = models.CharField(max_length=100)                 # 가입 방법   
    mtrt_int = models.TextField(blank=True, null=True)          # 만기 후 이자율
    spcl_cnd = models.TextField(blank=True, null=True)          # 우대조건
    join_deny = models.IntegerField(blank=True, null=True)      # 가입제한
    join_member = models.TextField(blank=True, null=True)       # 가입대상
    etc_note = models.TextField(blank=True, null=True)          # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True)      # 최고한도
    dcls_strt_day = models.IntegerField(blank=True, null=True)  # 공시 시작일
    dcls_end_day = models.IntegerField(blank=True, null=True)   # 공시 종료일
    
class DepositOption(models.Model):                                                      # 예금 상품 옵션          
    deposit_product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name="options")      # 예금 상품
    dcls_month = models.CharField(max_length=20)                                        # 공시 제출월
    fin_co_no = models.CharField(max_length=100)                                        # 금융회사 코드
    intr_rate_type = models.CharField(max_length=100)                                   # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)                                # 저축 금리 유형명
    save_trm = models.IntegerField()                                                    # 저축 기간
    intr_rate = models.FloatField(default=-1)                                           # 저축 금리
    intr_rate2 = models.FloatField(default=-1)                                          # 최고 우대 금리

class SavingProducts(models.Model):                             # 적금 상품
    dcls_month = models.CharField(max_length=20)                # 공시 제출월
    fin_co_no = models.CharField(max_length=100)                # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)                # 금융회사 명
    fin_prdt_cd = models.CharField(max_length=100)              # 금융상품 코드 
    fin_prdt_nm = models.CharField(max_length=100)              # 금융상품 명
    join_way = models.CharField(max_length=100)                 # 가입 방법   
    mtrt_int = models.TextField(blank=True, null=True)          # 만기 후 이자율
    spcl_cnd = models.TextField(blank=True, null=True)          # 우대조건
    join_deny = models.IntegerField(blank=True, null=True)      # 가입제한
    join_member = models.TextField(blank=True, null=True)       # 가입대상
    etc_note = models.TextField(blank=True, null=True)          # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True)      #최고한도
    dcls_strt_day = models.IntegerField(blank=True, null=True)  # 공시 시작일
    dcls_end_day = models.IntegerField(blank=True, null=True)   # 공시 종료일

class SavingOption(models.Model):                                                       # 적금 상품 옵션
    saving_product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name="options")        # 적금 상품
    dcls_month = models.CharField(max_length=20)                                        # 공시 제출월
    fin_co_no = models.CharField(max_length=100)                                        # 금융회사 코드
    intr_rate_type = models.CharField(max_length=100)                                   # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)                                # 저축 금리 유형명
    rsrv_type = models.CharField(max_length=100)                                        # 적립 유형
    rsrv_type_nm = models.CharField(max_length=100)                                     # 적립 유형명
    save_trm = models.IntegerField()                                                    # 저축 기간
    intr_rate = models.FloatField(default=-1)                                           # 저축 금리
    intr_rate2 = models.FloatField(default=-1)                                          # 최고 우대 금리

# 대출 상품
class LoanProducts(models.Model):                             # 대출 상품
    dcls_month = models.CharField(max_length=20)                # 공시 제출월
    fin_co_no = models.CharField(max_length=100)                # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)                # 금융회사 명
    fin_prdt_cd = models.CharField(max_length=100)              # 금융상품 코드 
    fin_prdt_nm = models.CharField(max_length=100)              # 금융상품 명
    join_way = models.CharField(max_length=100)                 # 가입 방법   
    crdt_prdt_type = models.CharField(max_length=100, blank=True, null=True)          # 대출 종류 코드
    crdt_prdt_type_nm = models.CharField(max_length=100)                 # 대출 종류명   
    cb_name = models.CharField(max_length=100)                 # CB 회사명   
    dcls_strt_day = models.IntegerField(blank=True, null=True)  # 공시 시작일
    dcls_end_day = models.IntegerField(blank=True, null=True)   # 공시 종료일
    fin_co_subm_day = models.IntegerField(blank=True, null=True)   # 금융회사 제출 월일

class LoanOption(models.Model):                                                       # 대출 상품 옵션
    fin_co_no = models.CharField(max_length=100)                # 금융 회사 코드 (**)
    fin_prdt_cd = models.CharField(max_length=100)                # 금융 상품 코드 (**)
    dcls_month = models.CharField(max_length=20)                # 공시 제출월 (**)
    crdt_lend_rate_type = models.CharField(max_length=20)                       # 금리 구분 코드
    crdt_lend_rate_type_nm = models.CharField(max_length=20)                       # 금리 구분
    crdt_grad_1 = models.FloatField(blank=True, null=True)                                    # 900점 초과 (신용 등급)
    crdt_grad_4 = models.FloatField(blank=True, null=True)                                       # 801~900
    crdt_grad_5 = models.FloatField(blank=True, null=True)                                       # 701~800
    crdt_grad_6 = models.FloatField(blank=True, null=True)                                       # 601~700
    crdt_grad_10 = models.FloatField(blank=True, null=True)                                      # 501~600
    crdt_grad_11 = models.FloatField(blank=True, null=True)                                      # 401~500
    crdt_grad_12 = models.FloatField(blank=True, null=True)                                      # 301~400
    crdt_grad_13 = models.FloatField(blank=True, null=True)                                      # 300 이하
    crdt_grad_avg = models.FloatField(default=-1)                                     # 평균 금리
    


class LoanTotal(models.Model):                             # 대출 상품
    dcls_month = models.CharField(max_length=20)                # 공시 제출월
    fin_co_no = models.CharField(max_length=100)                # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)                # 금융회사 명
    fin_prdt_cd = models.CharField(max_length=100)              # 금융상품 코드 
    fin_prdt_nm = models.CharField(max_length=100)              # 금융상품 명
    join_way = models.CharField(max_length=100)                 # 가입 방법   
    crdt_prdt_type = models.CharField(max_length=100, blank=True, null=True)          # 대출 종류 코드
    crdt_prdt_type_nm = models.CharField(max_length=100)                 # 대출 종류명   
    cb_name = models.CharField(max_length=100)                 # CB 회사명   
    dcls_strt_day = models.IntegerField(blank=True, null=True)  # 공시 시작일
    dcls_end_day = models.IntegerField(blank=True, null=True)   # 공시 종료일
    fin_co_subm_day = models.IntegerField(blank=True, null=True)   # 금융회사 제출 월일
    crdt_lend_rate_type = models.CharField(max_length=20, blank=True, null=True)              # 금리 구분 코드
    crdt_lend_rate_type_nm = models.CharField(max_length=20, blank=True, null=True)           # 금리 구분
    crdt_grad_1 = models.FloatField(blank=True, null=True)                                    # 900점 초과 (신용 등급)
    crdt_grad_4 = models.FloatField(blank=True, null=True)                                       # 801~900
    crdt_grad_5 = models.FloatField(blank=True, null=True)                                       # 701~800
    crdt_grad_6 = models.FloatField(blank=True, null=True)                                       # 601~700
    crdt_grad_10 = models.FloatField(blank=True, null=True)                                      # 501~600
    crdt_grad_11 = models.FloatField(blank=True, null=True)                                      # 401~500
    crdt_grad_12 = models.FloatField(blank=True, null=True)                                      # 301~400
    crdt_grad_13 = models.FloatField(blank=True, null=True)                                      # 300 이하
    crdt_grad_avg = models.FloatField(default=-1)                                     # 평균 금리