# Step 1: Build the Vue3 app
FROM node:18-alpine AS build

# 작업 디렉토리 설정
WORKDIR /app

# Vue 프로젝트 복사
COPY vue-pjt /app/vue-pjt

# 작업 디렉토리 이동
WORKDIR /app/vue-pjt

# 패키지 파일 복사
COPY package*.json ./ 

# 의존성 설치
RUN npm install

# 환경변수 주입
ARG VITE_API_KEY_KAKAO_JS 
ENV VITE_API_KEY_KAKAO_JS=$VITE_API_KEY_KAKAO_JS

# 빌드 실행
RUN npm run build

# Step 2: Serve the app with Nginx
FROM nginx:1.23.4-alpine

# Cloud Run의 PORT 환경 변수 사용
ENV PORT 8080

# Nginx 설정 복사
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 빌드 결과물 복사
COPY --from=build /app/vue-pjt/dist /usr/share/nginx/html

# Nginx 기본 설정 파일에서 ${PORT} 환경 변수를 동적으로 대체
RUN sed -i "s/listen 80;/listen ${PORT};/" /etc/nginx/conf.d/default.conf

# Cloud Run에 노출할 포트 설정
EXPOSE 8080

# Nginx 실행
CMD ["nginx", "-g", "daemon off;"]
