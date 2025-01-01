<template>
  <div class='coredream-regular'>
    <h5 class='coredream-bold'>게시글 수정</h5>
    <div v-if="article" class='coredream-regular'>
      <form @submit.prevent="updateArticle">

          <label for="title" class="form-label">제목</label>
          <input
            type="text"
            id="title"
            v-model="article.title"
            class="form-control"
          />


          <label for="content" class="form-label">내용</label>
          <textarea
            id="content"
            v-model="article.content"
            class="form-control"
            rows="5"
          ></textarea>

        <button type="submit" class="btn btn-primary">수정하기</button>
        <button type="button" class="btn btn-secondary" @click="cancelEdit">
          취소
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const route = useRoute();
const router = useRouter();
const article = ref(null);

// 게시글 상세 정보 로드 함수
const loadArticleDetail = function () {
  axios({
    method: 'get',
    url: `${store.BASE_URL}/api/v3/articles/${route.params.id}/`,
    headers: store.header,
  })
    .then((res) => {
      article.value = res.data
      console.log('게시글 작성 성공!')
    })
    .catch((err) => {
      console.log(err)
    })
}

// 게시글 수정 함수
const updateArticle = function () {
  axios({
    method: 'put',
    url: `${store.BASE_URL}/api/v3/articles/${route.params.id}/`,
    headers: store.header,
    data: {
      title: title.value,
      content: content.value
    },
  })
    .then((res) => {
      console.log("게시글 수정 성공!");
      router.push({ name: "ArticleDetail", params: { id: route.params.id } });
    })
    .catch((err) => {
      console.log(err)
    })
}


// 취소 버튼 클릭 시 상세 페이지로 돌아가는 함수
const cancelEdit = () => {
  router.push({ name: "ArticleDetail", params: { id: route.params.id } });
};

// 컴포넌트가 마운트되면 게시글 상세 정보 로드
onMounted(() => {
  loadArticleDetail();
});
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


/* 전체 컨테이너 */
div {
  font-family: 'Arial', sans-serif;
  max-width: 600px;
  margin: 40px auto;
  padding: 30px;
  background-color: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 15px;
}

/* 제목 스타일 */
h1 {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  color: #203359; /* 네이비 */
  margin-bottom: 30px;
}

/* 폼 요소 */
form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

label {
  font-size: 1rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 10px;
  font-size: 1rem;
  box-sizing: border-box;
  background-color: #f9f9f9;
}

textarea {
  resize: none; /* 크기 조정 방지 */
}

/* 버튼 컨테이너 */
button {
  padding: 12px 20px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button.btn-primary {
  background-color: #203359; /* 네이비 */
  color: #fff;
  border: none;
}

button.btn-primary:hover {
  background-color: #0d1a2e; /* 더 짙은 네이비 */
}

button.btn-secondary {
  background-color: #6c757d; /* 회색 */
  color: #fff;
  border: none;
  margin-top: 10px;
}

button.btn-secondary:hover {
  background-color: #5a6268;
}

/* 버튼 정렬 */
form > button {
  width: 100%; /* 버튼을 전체 너비로 설정 */
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  div {
    padding: 20px;
  }

  h1 {
    font-size: 1.8rem;
  }

  input[type="text"],
  textarea {
    font-size: 0.9rem;
    padding: 12px;
  }

  button {
    font-size: 0.9rem;
    padding: 10px 15px;
  }
}
</style>

