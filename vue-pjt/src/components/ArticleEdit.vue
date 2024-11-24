<template>
  <div>
    <h1>게시글 수정</h1>
    <div v-if="article">
      <form @submit.prevent="updateArticle">
        <div class="mb-3">
          <label for="title" class="form-label">제목</label>
          <input
            type="text"
            id="title"
            v-model="article.title"
            class="form-control"
          />
        </div>
        <div class="mb-3">
          <label for="content" class="form-label">내용</label>
          <textarea
            id="content"
            v-model="article.content"
            class="form-control"
            rows="5"
          ></textarea>
        </div>
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

const BASE_URL = "http://127.0.0.1:8000";
const route = useRoute();
const router = useRouter();
const article = ref(null);

// 게시글 상세 정보 로드 함수
const loadArticleDetail = async () => {
  try {
    const response = await axios.get(
      `${BASE_URL}/api/v3/articles/${route.params.id}/`
    );
    article.value = response.data;
  } catch (error) {
    console.error("게시글 상세 로드 중 오류 발생:", error);
  }
};

// 게시글 수정 함수
const updateArticle = async () => {
  try {
    await axios.put(`${BASE_URL}/api/v3/articles/${route.params.id}/`, {
      title: article.value.title,
      content: article.value.content,
    });
    console.log("게시글 수정 성공!");
    router.push({ name: "ArticleDetail", params: { id: route.params.id } });
  } catch (error) {
    console.error("게시글 수정 중 오류 발생:", error);
    alert("게시글 수정에 실패했습니다. 다시 시도해주세요.");
  }
};

// 취소 버튼 클릭 시 상세 페이지로 돌아가는 함수
const cancelEdit = () => {
  router.push({ name: "ArticleDetail", params: { id: route.params.id } });
};

// 컴포넌트가 마운트되면 게시글 상세 정보 로드
onMounted(() => {
  loadArticleDetail();
});
</script>

<style>
/* 필요에 따라 스타일링 추가 */
</style>
