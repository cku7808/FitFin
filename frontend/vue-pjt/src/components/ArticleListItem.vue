<template>
    <div>
      <p><RouterLink :to="{ name: 'ArticleDetail', params: { id: article.id } }">{{ article.title }}</RouterLink></p>
      <p>{{ article.content }}</p>
      
      <hr>
    </div>
  </template>
  
  <script setup>
  import { RouterLink } from 'vue-router'
  
  defineProps({
    article: Object
  })
  </script>
  
  <style scoped>
/* 전체 컨테이너 */
div {
  padding: 15px;
  margin-bottom: 15px;
  background-color: #f9f9f9; /* 연한 회색 배경 */
  border: 1px solid #e0e0e0; /* 테두리 */
  border-radius: 10px; /* 둥근 모서리 */
  transition: transform 0.3s, box-shadow 0.3s;
}

/* 호버 효과 */
div:hover {
  transform: translateY(-5px); /* 살짝 들어올리기 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* 그림자 효과 */
}

/* 게시글 ID */
h5 {
  font-size: 1rem;
  font-weight: bold;
  color: #6c757d; /* 회색 톤 */
  margin-bottom: 10px;
}

/* 게시글 제목 */
p a {
  font-size: 1.2rem;
  font-weight: bold;
  color: #203359; /* 네이비 */
  text-decoration: none; /* 밑줄 제거 */
  transition: color 0.3s ease;
}

p a:hover {
  color: #0d1a2e; /* 더 짙은 네이비 */
  text-decoration: underline; /* 호버 시 밑줄 추가 */
}

/* 게시글 내용 */
p {
  font-size: 1rem;
  color: #555; /* 중간 회색 */
  margin-top: 5px;
  line-height: 1.5;
}

/* 구분선 */
hr {
  border: 1px solid #e0e0e0;
  margin-top: 15px;
  margin-bottom: 0;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  div {
    padding: 10px;
  }

  h5 {
    font-size: 0.9rem;
  }

  p a {
    font-size: 1rem;
  }

  p {
    font-size: 0.9rem;
  }
}
</style>
