# Python 베이스 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Django 프로젝트 소스 코드 복사
COPY django-pjt /app/django-pjt

# STATIC_ROOT 디렉토리 생성 및 정적 파일 수집
WORKDIR /app/django-pjt
RUN mkdir -p /app/django-pjt/staticfiles
ENV SECRET_KEY=dummy-secret-key-for-build

# makemigrations 및 collectstatic 실행
RUN python manage.py makemigrations --noinput
RUN python manage.py collectstatic --noinput

# Gunicorn 실행
CMD ["bash", "-c", "python manage.py migrate && gunicorn fitfin.wsgi:application --bind 0.0.0.0:8080"]
