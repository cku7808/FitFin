from django.shortcuts import render

# Create your views here.
from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets, status
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialLoginView
import requests
from allauth.socialaccount.models import SocialAccount
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

@api_view(['POST'])
def login(request):
    user = authenticate_user(request)
    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'access': access_token,
            'refresh': refresh_token,
            'user': user_data(user),
        })
    else:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def social_login(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(email=email, username=email)

    # JWT 토큰 발급
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })
