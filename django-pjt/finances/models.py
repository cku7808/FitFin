from django.db import models

# Create your models here.

# 환율 (일 데이터만 저장 - 매일 11시 업데이트)
class Currency(models.Model):
    cur_unit = models.CharField(max_length=100)         # 통화코드
    cur_nm = models.CharField(max_length=100)           # 국가/통화명
    ttb = models.CharField(max_length=100)              # 전신환(송금) 받으실때
    tts = models.CharField(max_length=100)              # 전신환(송금) 보내실때
    deal_bas_r = models.CharField(max_length=100)       # 매매 기준율
    bkpr = models.CharField(max_length=100)             # 장부 가격
    yy_efee_r = models.CharField(max_length=100)        # 년환가료율
    ten_dd_efee_r = models.CharField(max_length=100)    # 10일환가료율
    kftc_deal_bas_r = models.CharField(max_length=100)  # 서울외국환중개 매매 기준율
    kftc_bkpr = models.CharField(max_length=100)        # 서울외국환중개 장부 가격


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
