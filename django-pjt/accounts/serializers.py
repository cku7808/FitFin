from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class CustomRegisterSerializer(RegisterSerializer):
    # 필요한 필드들을 추가합니다.
    income = serializers.IntegerField(required=True)
    assets = serializers.IntegerField(required=True)
    is_married = serializers.BooleanField(required=True)
    job = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    
    # def validate(self, data):
    #     # 부모 클래스의 validate 호출 (비밀번호 일치 검사 유지)
    #     data = super().validate(data)
    #     return data
    
    # # 데이터를 저장하도록 get_cleaned_data를 수정
    # def get_cleaned_data(self):
    #     cleaned_data = super().get_cleaned_data()  # 기존 데이터를 가져옵니다.
    #     cleaned_data.update({
    #         'income': self.validated_data.get('income', 0),
    #         'assets': self.validated_data.get('assets', 0),
    #         'is_married': self.validated_data.get('is_married', False),
    #         'job': self.validated_data.get('job', ""),
    #         'age': self.validated_data.get('age', 0),
    #     })
    #     return cleaned_data
    
    # # 저장 메서드 오버라이드
    # def save(self, request):
    #     user = super().save(request)  # 기본 사용자 생성 로직
    #     user.income = self.validated_data.get('income', 0)
    #     user.assets = self.validated_data.get('assets', 0)
    #     user.is_married = self.validated_data.get('is_married', False)
    #     user.job = self.validated_data.get('job', "")
    #     user.age = self.validated_data.get('age', 0)
    #     user.save()
    #     return user
