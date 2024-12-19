from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# 프로필 이미지 (저장하는 파일명 변경)
import os
from uuid import uuid4
from django.utils import timezone

def upload_to_profile(instance, filename):
    # 파일 확장자 추출
    extension = filename.split('.')[-1]
    # 새로운 파일명 생성 (UUID + 현재 시간)
    new_filename = f"profile_{uuid4().hex[:10]}_{timezone.now().strftime('%Y%m%d%H%M%S')}.{extension}"
    # 저장 경로 반환
    return os.path.join('profile_images/', new_filename)

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
    
    # def save(self, *args, **kwargs):
    #     # If the instance already exists in the database
    #     if self.pk:
    #         old_user = User.objects.filter(pk=self.pk).first()
    #         if old_user and old_user.profile_img != self.profile_img:
    #             # If the old image is not the default image, delete it
    #             if old_user.profile_img and old_user.profile_img.name != 'accounts/profile.png':
    #                 if os.path.isfile(old_user.profile_img.path):
    #                     old_user.profile_img.delete(save=False)
        
    #     super().save(*args, **kwargs)
    credit = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(1000)], default=0)

    profile_img = models.ImageField(blank=True, null=True, 
                                    default='static/accounts/profile.png',
                                    upload_to=upload_to_profile)
