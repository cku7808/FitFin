<template>
  <div class="coredream-regular">
    <h5 class="coredream-bold">게시글 작성</h5>
    <form @submit.prevent="createArticle">
      <div class="coredream-regular">
        <label for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title">
      </div>
      <div class="coredream-regular">
        <label for="content">내용 : </label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const title = ref(null)
const content = ref(null)
const router = useRouter()
const newArticleId = ref(null)

// DRF로 게시글 생성 요청을 보내는 함수
const createArticle = function () {
  axios({
    method: 'post',
    url: `${store.BASE_URL}/api/v3/articles/`,
    headers: store.header,
    data: {
      title: title.value,
      content: content.value
    }
  })
    .then((res) => {
      console.log('게시글 작성 성공!')
      newArticleId.value = res.data.articleid
      router.push({ name: 'ArticleDetail', params: { id: newArticleId.value } })
    })
    .catch((err) => {
      console.log(err)
    })
}

</script>

<style scoped>
@font-face {
    font-family: 'S-CoreDream-3Light';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/S-CoreDream-3Light.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.coredream-bold {
font-family: 'S-CoreDream-3Light';
font-weight: bold;
font-style: normal;
}

.coredream-regular {
font-family: 'S-CoreDream-3Light';
font-weight: 400;
font-style: normal;
}

.coredream-semibold {
font-family: 'S-CoreDream-3Light';
font-weight: 600;
font-style: normal;
}


/* 전체 레이아웃 */
div {
  font-family: 'Arial', sans-serif;
  max-width: 800px;
  margin: 0 auto; /* 중앙 정렬 */
  padding: 20px;
  border: 1px solid #e0e0e0; /* 연한 테두리 */
  border-radius: 8px; /* 모서리 둥글게 */
  background-color: #fff; /* 배경 흰색 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 박스 그림자 */
}

/* 제목 */
h1 {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  color: #203359; /* 네이비 */
  margin-bottom: 20px;
}

/* 폼 요소 */
form div {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 1rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  box-sizing: border-box;
}

textarea {
  height: 120px;
  resize: none; /* 크기 조정 방지 */
}

input[type="submit"] {
  width: 100%;
  padding: 10px;
  background-color: #203359; /* 네이비 */
  color: #fff; /* 텍스트 흰색 */
  border: none;
  border-radius: 5px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
  background-color: #0d1a2e; /* 더 짙은 네이비 */
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  div {
    padding: 15px;
  }

  h1 {
    font-size: 1.8rem;
  }

  input[type="submit"] {
    font-size: 1rem;
  }
}
</style>
