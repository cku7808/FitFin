from django.shortcuts import render

# Create your views here.
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.http import JsonResponse

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # 요청에서 username과 password 가져오기
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
        })
    else:
        return Response({
            'message': '유효하지 않은 사용자 정보입니다.'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def social_login(request):
    email = request.data.get('email')
    print(email)
    try:
        user = User.objects.get(email=email)
        print(user)
    except User.DoesNotExist:
        return Response({
            'message': '가입되지 않은 사용자입니다.'
        }, status.HTTP_400_BAD_REQUEST)

    # JWT 토큰 발급
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })

# 상품 가입
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def signup_products(request):
    user = request.user
    product_id = request.data.get('product_id')
    option_id = request.data.get('option_id')

    if not isinstance(user.registered_ptcd, list):
            user.registered_ptcd = []  # 초기화

    if (product_id, option_id) not in user.registered_ptcd:  # 중복 방지
        user.registered_ptcd.append((product_id, option_id))

    user.save()  # 변경사항 저장
    return Response({
        "message": "상품 가입이 완료되었습니다.",
        "registered_ptcd": user.registered_ptcd
    }, status=status.HTTP_200_OK)

# 상품 해지    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_products(request):
    user = request.user
    product_id = request.data.get('product_id')
    option_id = request.data.get('option_id')

    if [product_id, option_id] in user.registered_ptcd:  # 중복 방지
        test = '있음'
        user.registered_ptcd.remove([product_id, option_id])
    else:
        test = [product_id, option_id]

    user.save()  # 변경사항 저장
    return Response({
        "message": "상품 해지가 완료되었습니다.",
        "registered_ptcd": user.registered_ptcd,
        "test": test,
    }, status=status.HTTP_200_OK)



# 회원 정보
from uuid import uuid4

def upload_to_profile(instance, filename):
    # 파일 확장자 추출
    extension = filename.split('.')[-1]
    # 새로운 파일명 생성 (UUID + 현재 시간)
    new_filename = f"profile_{uuid4().hex[:10]}_{timezone.now().strftime('%Y%m%d%H%M%S')}.{extension}"
    # 저장 경로 반환
    return os.path.join('profile_images/', new_filename)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            if 'profile_img' in request.FILES:
                profile_img = request.FILES['profile_img']

                # 파일명 생성 및 저장
                file_path = upload_to_profile(user, profile_img.name)  # 경로 생성
                saved_path = default_storage.save(file_path, profile_img)  # GCS에 파일 저장
                file_url = default_storage.url(saved_path)  # URL 생성

                # URL을 serializer에 추가
                serializer.validated_data['profile_img'] = file_url
            serializer.save()
            return Response(status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "회원탈퇴가 완료되었습니다."}, status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def id_check(request):
    username = request.data.get('username')
    print('username', username)
    if User.objects.filter(username=username).exists():
        return Response({"message":"이미 존재하는 ID"}, status.HTTP_400_BAD_REQUEST)
    return Response({"message":"사용 가능한 ID"}, status.HTTP_200_OK)
