<template>
    <div>
        <h3>Article List</h3>
        <button type="button" class="btn btn-primary" @click="createarticle">작성하기</button>
        <hr>
        <ArticleListItem
        v-for="article in articlelist"
        :key="article.id"
        :article="article"/>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRouter } from "vue-router";


import ArticleListItem from '@/components/ArticleListItem.vue';

// 데이터 로드
const router = useRouter();
const BASE_URL = 'http://127.0.0.1:8000'
const articlelist = ref([])
const loadArticleList = function () {
    axios({
        method: 'get',
        url: `${BASE_URL}/api/v3/articles/`,
    })
    .then((res) => {
        articlelist.value = res.data
        console.log(articlelist.value)
    })
    .catch((err) => {
        console.log(err)
    })
}
onMounted(() => {
    loadArticleList()
});


const createarticle = () => {
  router.push({ name: "ArticleCreate"});
}


</script>

<style scoped>
/* 전체 컨테이너 */
div {
  font-family: 'Arial', sans-serif;
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

/* 페이지 제목 */
h3 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #203359; /* 네이비 */
  text-align: center;
  margin-bottom: 20px;
}

/* 작성하기 버튼 */
button.btn-primary {
  display: block;
  margin: 0 auto 20px auto; /* 버튼을 중앙 정렬 */
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  background-color: #203359;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button.btn-primary:hover {
  background-color: #0d1a2e; /* 더 짙은 네이비 */
}

/* 게시글 리스트 */
hr {
  border: 1px solid #e0e0e0;
  margin: 20px 0;
}

/* 게시글 아이템 카드 */
.article-list-item {
  display: flex;
  flex-direction: column;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.article-list-item:hover {
  transform: translateY(-5px); /* 호버 시 카드 살짝 올라감 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* 그림자 효과 */
}

/* 게시글 제목 */
.article-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #203359;
  margin-bottom: 10px;
}

/* 게시글 내용 */
.article-content {
  font-size: 1rem;
  color: #555;
  line-height: 1.5;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  div {
    padding: 15px;
  }

  h3 {
    font-size: 1.6rem;
  }

  button {
    font-size: 0.9rem;
    padding: 8px 15px;
  }

  .article-title {
    font-size: 1rem;
  }

  .article-content {
    font-size: 0.9rem;
  }
}
</style>
