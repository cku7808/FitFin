from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# 프로필 이미지 (저장하는 파일명 변경)
import os




# 소득 수준
# 소비 성향
# 자산
# 미혼/기혼
# 직업
# 나이

# Create your models here.
class User(AbstractUser):
    # 데이터는 리스트 형식이나 저장은 json으로 변환하여 str type 
    # 1. 상품 가입 시 저장된 str 데이터들을 json 형식으로 load
    # 2. 리스트에 데이터 추가 후 json dump 하여 DB에 다시 저장 
    registered_ptcd = models.JSONField(default=list)
    income = models.IntegerField(default=0)
    # consume_tendency = models.se
    assets = models.IntegerField(default=0) # 기본 1만원
    is_married = models.BooleanField(default=False)
    job = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    registered_loan = models.JSONField(default=list)

    credit = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(1000)], default=0)

    profile_img = models.ImageField(blank=True, null=True, 
                                    default='static/accounts/profile.png',
                                    upload_to='profile_images/')
